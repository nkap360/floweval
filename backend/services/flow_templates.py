import json
import logging
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, ValidationError

from .auth import require_user
from ..core.models import FlowEdge, FlowNode

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/flow-engine",
    tags=["flow-engine"],
    dependencies=[Depends(require_user())],
)


def _find_templates_directory() -> Path:
    """
    Find the templates directory across different deployment environments.
    
    Returns:
        Path: The path to the templates directory
        
    Raises:
        HTTPException: If templates directory cannot be found
    """
    # List of possible paths in order of preference
    possible_paths = [
        Path("/flow_engine/templates"),  # Docker absolute path
        Path("/app/flow_engine/templates"),  # Leapcell/alternative
        # Relative to backend module
        Path(__file__).parent.parent.parent / "flow_engine" / "templates",
        Path.cwd() / "flow_engine" / "templates",  # Current dir
        Path.cwd().parent / "flow_engine" / "templates",  # Parent dir
    ]
    
    logger.info("[FLOW_TEMPLATES] Searching for templates directory...")
    
    for path in possible_paths:
        logger.debug(
            "[FLOW_TEMPLATES] Checking path: %s (exists: %s)",
            path,
            path.exists()
        )
        if path.exists() and path.is_dir():
            logger.info(
                "[FLOW_TEMPLATES] Found templates directory: %s",
                path
            )
            return path
    
    # If not found, log all attempted paths and working directory
    logger.error(
        "[FLOW_TEMPLATES] Templates directory not found!"
    )
    logger.error(
        "Current working directory: %s",
        Path.cwd()
    )
    logger.error(
        "Script location: %s",
        Path(__file__).parent
    )
    logger.error(
        "Attempted paths: %s",
        [str(p) for p in possible_paths]
    )
    
    # List contents of common parent directories for debugging
    for base_path in [Path("/"), Path("/app"), Path.cwd()]:
        if base_path.exists():
            try:
                contents = list(base_path.iterdir())[:20]  # Limit to 20
                logger.error(
                    "Contents of %s: %s",
                    base_path,
                    [p.name for p in contents]
                )
            except (OSError, PermissionError) as e:
                logger.error(
                    "Cannot list contents of %s: %s",
                    base_path,
                    str(e)
                )
    
    raise HTTPException(
        status_code=500,
        detail="Templates directory not found in any expected location"
    )


# Find templates directory at module load time
TEMPLATES_DIR = _find_templates_directory()
FLOW_ENGINE_DIR = TEMPLATES_DIR.parent

logger.info(
    "FLOW_ENGINE_DIR: %s | TEMPLATES_DIR: %s",
    FLOW_ENGINE_DIR,
    TEMPLATES_DIR
)


class FlowTemplate(BaseModel):
    id: str
    name: str
    description: str | None = None
    category: str | None = None
    nodes: List[FlowNode]
    edges: List[FlowEdge]


def _load_template(path: Path) -> FlowTemplate:
    logger.debug("[FLOW_TEMPLATES] Loading template from: %s", path)
    try:
        payload = json.loads(path.read_text())
        logger.debug(
            "[FLOW_TEMPLATES] Successfully parsed JSON from %s | Keys: %s",
            path.name,
            list(payload.keys())
        )
        template = FlowTemplate(**payload)
        logger.info(
            "[FLOW_TEMPLATES] Successfully loaded template: %s (ID: %s)",
            template.name,
            template.id
        )
        return template
    except ValidationError as exc:  # pragma: no cover - defensive guardrail
        logger.error(
            "[FLOW_TEMPLATES] Validation error for %s | Error: %s",
            path.name,
            str(exc),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Invalid flow template {path.name}: {exc}",
        ) from exc
    except json.JSONDecodeError as exc:
        # pragma: no cover - defensive guardrail
        logger.error(
            "[FLOW_TEMPLATES] JSON decode error for %s | Error: %s",
            path.name,
            str(exc),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Flow template {path.name} is not valid JSON",
        ) from exc
    except Exception as exc:
        logger.error(
            "[FLOW_TEMPLATES] Unexpected error loading %s",
            path.name,
            exc_info=True
        )
        logger.error(
            "Type: %s | Error: %s",
            type(exc).__name__,
            str(exc)
        )
        raise


@router.get("/templates", response_model=List[FlowTemplate])
async def list_templates() -> List[FlowTemplate]:
    logger.info(
        "[FLOW_TEMPLATES] Listing templates request"
    )
    logger.info(
        "TEMPLATES_DIR: %s | Exists: %s | Is dir: %s",
        TEMPLATES_DIR,
        TEMPLATES_DIR.exists(),
        TEMPLATES_DIR.is_dir() if TEMPLATES_DIR.exists() else False
    )
    
    # Check parent directory
    if not FLOW_ENGINE_DIR.exists():
        logger.error(
            "[FLOW_TEMPLATES] Flow engine directory does not exist: %s",
            FLOW_ENGINE_DIR
        )
        raise HTTPException(
            status_code=404,
            detail=f"Flow engine directory not found: {FLOW_ENGINE_DIR}"
        )
    
    # Check templates directory
    if not TEMPLATES_DIR.exists():
        logger.error(
            "[FLOW_TEMPLATES] Templates directory does not exist: %s",
            TEMPLATES_DIR
        )
        logger.error(
            "Parent exists: %s | Parent contents: %s",
            FLOW_ENGINE_DIR.exists(),
            list(FLOW_ENGINE_DIR.iterdir())
            if FLOW_ENGINE_DIR.exists() else []
        )
        raise HTTPException(
            status_code=404,
            detail=f"Templates directory not found: {TEMPLATES_DIR}"
        )
    
    # List all files in templates directory
    try:
        all_files = list(TEMPLATES_DIR.iterdir())
        logger.info(
            "[FLOW_TEMPLATES] Templates directory contents"
        )
        logger.info(
            "Total files: %d | Files: %s",
            len(all_files),
            [f.name for f in all_files]
        )
    except Exception as e:
        logger.error(
            "[FLOW_TEMPLATES] Error reading templates directory | Error: %s",
            str(e),
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail=f"Error reading templates directory: {str(e)}"
        ) from e
    
    # Find JSON template files
    template_files = sorted(TEMPLATES_DIR.glob("*.json"))
    logger.info(
        "[FLOW_TEMPLATES] Found %d JSON template files: %s",
        len(template_files),
        [f.name for f in template_files]
    )
    
    if not template_files:
        logger.warning(
            "[FLOW_TEMPLATES] No JSON template files found in %s",
            TEMPLATES_DIR
        )
        raise HTTPException(
            status_code=404,
            detail=f"No flow templates found in {TEMPLATES_DIR}"
        )

    templates = [_load_template(path) for path in template_files]
    logger.info(
        "[FLOW_TEMPLATES] Successfully loaded %d templates",
        len(templates)
    )
    return templates
