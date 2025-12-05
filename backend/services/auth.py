import json
import logging
import os
from functools import lru_cache
from typing import Dict, List, Optional

import httpx
from fastapi import Depends, Header, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AuthSettings(BaseModel):
    supabase_jwt_secret: str = os.getenv("SUPABASE_JWT_SECRET", "dev-insecure-secret")
    supabase_url: Optional[str] = os.getenv("SUPABASE_URL")
    supabase_service_role_key: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    default_workspace_id: str = os.getenv("DEFAULT_WORKSPACE_ID", "ws-default")
    default_workspace_group_id: Optional[str] = os.getenv("DEFAULT_WORKSPACE_GROUP_ID", "grp-default-viewers")
    default_workspace_role: str = os.getenv("DEFAULT_WORKSPACE_ROLE", "viewer")
    disable_auth: bool = os.getenv("DISABLE_AUTH", "false").lower() == "true"

    @property
    def has_supabase_sync(self) -> bool:
        return bool(self.supabase_url and self.supabase_service_role_key)


class WorkspaceMembership(BaseModel):
    workspace_id: str
    group_id: Optional[str] = None
    role: str


class AuthenticatedUser(BaseModel):
    user_id: str
    email: Optional[str] = None
    memberships: Dict[str, WorkspaceMembership]
    is_platform_admin: bool = False


class AuthError(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


@lru_cache()
def get_settings() -> AuthSettings:
    settings = AuthSettings()
    if settings.supabase_jwt_secret == "dev-insecure-secret":
        logger.warning(
            "SUPABASE_JWT_SECRET not provided; using insecure development secret. "
            "Set SUPABASE_JWT_SECRET for production deployments."
        )
    return settings


def _extract_token(authorization: str) -> str:
    if not authorization:
        raise AuthError(status.HTTP_401_UNAUTHORIZED, "Authorization header required")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise AuthError(status.HTTP_401_UNAUTHORIZED, "Bearer token required")

    return token


def _decode_token(token: str, settings: AuthSettings) -> dict:
    try:
        # Supabase JWTs include audience claim
        # Disable verification to accept any audience
        return jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=["HS256"],
            options={"verify_aud": False}
        )
    except JWTError as exc:  # pragma: no cover - defensive guardrail
        logger.error("Failed to decode access token", exc_info=exc)
        raise AuthError(
            status.HTTP_401_UNAUTHORIZED, "Invalid access token"
        ) from exc


async def _fetch_memberships_from_supabase(
    user_id: str, settings: AuthSettings
) -> List[WorkspaceMembership]:
    if not settings.has_supabase_sync:
        return []

    memberships_url = f"{settings.supabase_url.rstrip('/')}/rest/v1/workspace_memberships"
    headers = {
        "apikey": settings.supabase_service_role_key,  # type: ignore[arg-type]
        "Authorization": f"Bearer {settings.supabase_service_role_key}",  # type: ignore[arg-type]
    }
    params = {"user_id": f"eq.{user_id}", "select": "workspace_id,group_id,role"}

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(memberships_url, headers=headers, params=params)

    if response.status_code != 200:
        logger.error(
            "Supabase membership lookup failed", extra={
                "status": response.status_code,
                "body": response.text,
            }
        )
        raise AuthError(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "Unable to validate workspace membership"
        )

    entries = response.json()
    return [WorkspaceMembership(**entry) for entry in entries]


def _load_memberships_from_claims(payload: dict) -> List[WorkspaceMembership]:
    embedded = (
        payload.get("workspace_roles")
        or payload.get("app_metadata", {}).get("workspace_roles")
    )
    if not embedded:
        return []

    memberships: List[WorkspaceMembership] = []
    for entry in embedded:
        try:
            memberships.append(WorkspaceMembership(**entry))
        except Exception as exc:  # pragma: no cover - defensive guardrail
            logger.warning(
                "Ignoring invalid workspace_roles claim", extra={"entry": entry, "error": str(exc)}
            )
    return memberships


async def _resolve_memberships(
    user_id: str, payload: dict, settings: AuthSettings, is_platform_admin: bool
) -> Dict[str, WorkspaceMembership]:
    memberships: List[WorkspaceMembership] = []

    embedded = _load_memberships_from_claims(payload)
    if embedded:
        memberships.extend(embedded)

    if settings.has_supabase_sync:
        try:
            remote_memberships = await _fetch_memberships_from_supabase(user_id, settings)
            # Merge remote over embedded to honor server truth
            merged: Dict[str, WorkspaceMembership] = {m.workspace_id: m for m in embedded}
            for membership in remote_memberships:
                merged[membership.workspace_id] = membership
            return merged
        except AuthError:
            # Surface upstream Supabase errors directly
            raise
        except Exception as exc:  # pragma: no cover - defensive guardrail
            logger.error("Unexpected Supabase lookup failure", exc_info=exc)
            raise AuthError(
                status.HTTP_503_SERVICE_UNAVAILABLE,
                "Unable to validate workspace membership",
            ) from exc
    resolved = {m.workspace_id: m for m in memberships}

    # If the user has no explicit memberships and is not a platform admin,
    # fall back to the default workspace so new users can immediately access
    # a space managed by the admin panel.
    if not resolved and not is_platform_admin and settings.default_workspace_id:
        resolved[settings.default_workspace_id] = WorkspaceMembership(
            workspace_id=settings.default_workspace_id,
            group_id=settings.default_workspace_group_id,
            role=settings.default_workspace_role,
        )

    return resolved


async def _build_auth_context(authorization: str | None = Header(None)) -> AuthenticatedUser:
    settings = get_settings()
    
    # Development bypass: only if auth is explicitly disabled
    if settings.disable_auth:
        logger.warning("Auth disabled - using dev user")
        return AuthenticatedUser(
            user_id="dev-user",
            email="dev@example.com",
            memberships={
                "default-workspace": WorkspaceMembership(
                    workspace_id="default-workspace",
                    role="admin"
                )
            },
            is_platform_admin=True,  # Make dev user a platform admin
        )
    
    # In production mode, require authorization header
    if not authorization:
        raise AuthError(status.HTTP_401_UNAUTHORIZED, "Authorization header required")
    
    token = _extract_token(authorization)
    payload = _decode_token(token, settings)

    user_id = payload.get("sub")
    if not user_id:
        raise AuthError(status.HTTP_401_UNAUTHORIZED, "Token missing subject (sub)")

    is_platform_admin = bool(
        payload.get("role") == "service_role"
        or payload.get("is_platform_admin")
        or payload.get("app_metadata", {}).get("platform_admin")
    )

    memberships = await _resolve_memberships(user_id, payload, settings, is_platform_admin)

    return AuthenticatedUser(
        user_id=user_id,
        email=payload.get("email"),
        memberships=memberships,
        is_platform_admin=is_platform_admin,
    )


def require_user():
    async def dependency(user: AuthenticatedUser = Depends(_build_auth_context)) -> AuthenticatedUser:
        return user

    return dependency


def require_workspace_role(allowed_roles: Optional[List[str]] = None):
    async def dependency(
        workspace_id: str = Header(..., alias="X-Workspace-Id"),
        user: AuthenticatedUser = Depends(_build_auth_context),
    ) -> AuthenticatedUser:
        membership = user.memberships.get(workspace_id)
        if not membership and not user.is_platform_admin:
            raise AuthError(status.HTTP_403_FORBIDDEN, "User not a member of this workspace")

        if allowed_roles and not user.is_platform_admin:
            if not membership or membership.role not in allowed_roles:
                raise AuthError(status.HTTP_403_FORBIDDEN, "Insufficient role for workspace")

        return user

    return dependency


def describe_auth_model() -> dict:
    """Expose current auth configuration for documentation and debugging."""

    settings = get_settings()
    return {
        "uses_supabase": settings.has_supabase_sync,
        "supabase_url": settings.supabase_url,
        "auth_strategy": "supabase_jwt",
    }
