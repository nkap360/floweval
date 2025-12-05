import json
import logging
from pathlib import Path
from typing import Literal, Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .auth import require_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/logs", tags=["logs"], dependencies=[Depends(require_user())])

# Define LOG_DIR relative to backend directory
LOG_DIR = Path(__file__).resolve().parent.parent.parent / "logs"
try:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    # Fallback to /tmp for serverless/read-only environments
    LOG_DIR = Path("/tmp/flowbuilder_logs")
    LOG_DIR.mkdir(parents=True, exist_ok=True)

FRONTEND_LOG_PATH = LOG_DIR / "frontend.log"


class FrontendLogEntry(BaseModel):
    level: Literal["debug", "info", "warn", "error"]
    message: str
    meta: Optional[dict] = None
    timestamp: str


@router.post("/frontend")
def ingest_frontend_log(entry: FrontendLogEntry):
    with FRONTEND_LOG_PATH.open("a", encoding="utf-8") as logfile:
        logfile.write(json.dumps(entry.dict()) + "\n")
    logger.info(
        "Frontend log captured: %s", entry.message, extra={"frontend_level": entry.level}
    )
    return {"status": "ok"}
