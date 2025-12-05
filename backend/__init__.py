import logging
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from rich.logging import RichHandler

load_dotenv()


def _resolve_log_level() -> int:
    env_level = os.getenv("BACKEND_LOG_LEVEL", "DEBUG").upper()
    level = logging._nameToLevel.get(env_level)  # type: ignore[attr-defined]
    if isinstance(level, int) and level > 0:
        return level

    fallback_level = logging.DEBUG
    logging.basicConfig(level=fallback_level)
    logging.getLogger(__name__).warning(
        "Invalid BACKEND_LOG_LEVEL=%s provided; defaulting to DEBUG", env_level
    )
    return fallback_level


LOG_DIR = Path(__file__).resolve().parent / "logs"
if not LOG_DIR.exists():
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
    except (PermissionError, OSError):
        # Fallback to /tmp if we can't create logs in backend dir
        # (e.g., read-only filesystem in serverless environments)
        LOG_DIR = Path("/tmp/flowbuilder_logs")
        LOG_DIR.mkdir(parents=True, exist_ok=True)

backend_log_path = LOG_DIR / "backend.log"

# Ensure backend modules emit informative logs when run under uvicorn
# or during local scripts with rich, colorful formatting and a file trace.
logging.basicConfig(
    level=_resolve_log_level(),
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        RichHandler(rich_tracebacks=True, markup=True),
        logging.FileHandler(backend_log_path, encoding="utf-8"),
    ],
)
