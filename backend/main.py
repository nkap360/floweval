"""
Flow Builder Backend API
========================
Backend entry point.

This module initializes the backend API server, loads all action modules,
configures middleware, and exposes REST endpoints for the Flow Builder UI.
"""

import logging
import os
import time
from importlib import import_module
from typing import Iterable

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import resend
from dotenv import load_dotenv

from .core.actions import get_actions_for_node_type
from .core.models import NodeType
from .services.auth import describe_auth_model, require_user
from .services.ai_proxy import router as ai_proxy_router
from .services.datasets import router as datasets_router
from .core.flow_executor import router as flow_router
from .services.flow_templates import router as flow_templates_router
from .services.logs import router as logs_router
from .config.logging_config import configure_logging

# Load environment variables
load_dotenv()

# Configure logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
configure_logging(level=LOG_LEVEL)

logger = logging.getLogger(__name__)
logger.info("Flow Builder Backend starting up...")
logger.info("Log level: %s", LOG_LEVEL)

ACTION_MODULES: Iterable[str] = (
    "actions.actions_crewai",
    "actions.actions_dataset",
    "actions.actions_deepeval",
)


def load_action_modules() -> None:
    """Import action modules for their registration side effects."""

    package = __name__.rsplit(".", 1)[0]
    for module_name in ACTION_MODULES:
        import_module(f"{package}.{module_name}")


load_action_modules()

app = FastAPI(title="Flow Builder Backend", version="0.1.0")

# Initialize Resend client
api_key = os.environ.get("RESEND_API_KEY")
resend.api_key = api_key


# Pydantic model for demo request
class DemoRequest(BaseModel):
    recipientEmail: str


# Demo credentials
DEMO_USER_EMAIL = 'user@example.com'
DEMO_PASSWORD = 'user'


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def validate_host(request: Request, call_next):
    """Validate that the request comes from an allowed host."""
    allowed_hosts = os.environ.get("ALLOWED_HOSTS", "")
    
    # If ALLOWED_HOSTS is not set or empty, allow all hosts
    if not allowed_hosts or allowed_hosts.strip() == "":
        return await call_next(request)
    
    # Parse allowed hosts from comma-separated string
    allowed_host_list = [host.strip() for host in allowed_hosts.split(",") if host.strip()]
    
    # Get the host from the request
    request_host = request.headers.get("host", "").split(":")[0]  # Remove port if present
    referer = request.headers.get("referer", "")
    origin = request.headers.get("origin", "")
    
    # Extract domain from referer or origin
    referer_host = ""
    if referer:
        # Extract domain from referer URL
        from urllib.parse import urlparse
        parsed = urlparse(referer)
        referer_host = parsed.netloc.split(":")[0]
    
    origin_host = ""
    if origin:
        from urllib.parse import urlparse
        parsed = urlparse(origin)
        origin_host = parsed.netloc.split(":")[0]
    
    # Check if request is from an allowed host
    is_allowed = (
        request_host in allowed_host_list or
        referer_host in allowed_host_list or
        origin_host in allowed_host_list or
        "localhost" in request_host or  # Always allow localhost for development
        "127.0.0.1" in request_host
    )
    
    if not is_allowed:
        logger.warning(
            "Blocked request from unauthorized host: %s (referer: %s, origin: %s)",
            request_host,
            referer_host,
            origin_host
        )
        raise HTTPException(
            status_code=403,
            detail="Access denied: Host not in allowed list"
        )
    
    return await call_next(request)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses with timing."""
    start_time = time.time()
    
    # Extract client information
    client_host = request.client.host if request.client else "unknown"
    client_port = request.client.port if request.client else 0
    
    # Log request details
    logger.info(
        ">>> INCOMING REQUEST: %s %s | Client: %s:%s | Query: %s",
        request.method,
        request.url.path,
        client_host,
        client_port,
        dict(request.query_params) if request.query_params else {}
    )
    logger.debug(
        "Request Headers: %s",
        {k: v for k, v in request.headers.items()
         if k.lower() not in ['authorization', 'cookie']}
    )
    
    try:
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        
        logger.info(
            "<<< RESPONSE: %s %s - Status: %d - Duration: %.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms
        )
        logger.debug(
            "Response Content-Type: %s",
            response.headers.get("content-type", "N/A")
        )
        
        return response
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.error(
            "<<< ERROR: %s %s - Exception: %s - Type: %s",
            request.method,
            request.url.path,
            str(e),
            type(e).__name__,
            exc_info=True
        )
        logger.error("Request duration: %.2fms", duration_ms)
        raise


@app.get(
    "/node-types/{node_type}/actions",
    dependencies=[Depends(require_user())]
)
def list_actions(node_type: NodeType):
    return get_actions_for_node_type(node_type)


@app.get("/auth/model")
def auth_model():
    """Introspect backend auth configuration for debugging."""

    return describe_auth_model()


@app.get("/health")
def health_check():
    """Health check endpoint for load balancers and monitoring."""
    return {
        "status": "healthy",
        "service": "flowbuilder-backend",
        "version": "0.1.0"
    }


@app.get("/kaithhealthcheck")
def kaith_health_check():
    """
    Leapcell.io health check endpoint.
    (kaith is their internal health check path)
    """
    return {
        "status": "ok",
        "service": "flowbuilder-backend",
        "timestamp": time.time()
    }


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Flow Builder API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


@app.post("/api/request-demo")
async def request_demo_credentials(request: DemoRequest):
    """Send demo credentials to the user's email via Resend."""
    recipient_email = request.recipientEmail

    if not recipient_email:
        raise HTTPException(status_code=400, detail="Recipient email is required")

    sender_email = os.environ.get("RESEND_SENDER_EMAIL")
    
    if not sender_email:
        raise HTTPException(status_code=500, detail="RESEND_SENDER_EMAIL not configured")

    try:
        # Send demo credentials directly to the user
        resend.Emails.send({
            "from": sender_email,
            "to": recipient_email,
            "subject": "Your Demo Credentials for Ground Truth Builder",
            "html": f"""
                <p>Hello,</p>
                <p>Thank you for requesting demo credentials for Ground Truth Builder.</p>
                <p>You can log in using the details below:</p>
                <div style="background-color: #f1f5f9; padding: 16px; border-radius: 4px; margin: 16px 0;">
                  <p><strong>Username:</strong> <code>{DEMO_USER_EMAIL}</code></p>
                  <p><strong>Password:</strong> <code>{DEMO_PASSWORD}</code></p>
                </div>
                <p>Access the application and start building your AI evaluation datasets!</p>
                <p>Best regards,<br>The Ground Truth Builder Team</p>
            """,
        })

        # Send notification to admin
        resend.Emails.send({
            "from": sender_email,
            "to": "titanicplus@gmail.com",
            "subject": "New Demo Credential Request",
            "html": f"""
                <p>A user requested demo credentials:</p>
                <p><strong>Email:</strong> {recipient_email}</p>
            """,
        })

        logger.info("Demo credentials sent to %s", recipient_email)
        return {"message": "Demo credentials sent! Check your email."}

    except Exception as e:
        logger.error("Resend error: %s", e)
        raise HTTPException(status_code=500, detail="Failed to send emails") from e


def include_routes(application: FastAPI):
    application.include_router(ai_proxy_router)
    application.include_router(datasets_router)
    application.include_router(flow_router)
    application.include_router(flow_templates_router)
    application.include_router(logs_router)


include_routes(app)
