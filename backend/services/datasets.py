import uuid
from pathlib import Path
from typing import Dict

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .auth import require_workspace_role

router = APIRouter(
    prefix="/datasets", tags=["datasets"], dependencies=[Depends(require_workspace_role())]
)

DATA_DIR = Path("/app/data")
try:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
except (PermissionError, OSError):
    # Fallback to /tmp if /app/data is not writable (e.g., serverless/read-only FS)
    DATA_DIR = Path("/tmp/flowbuilder_data")
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# In-memory dataset registry; replace with persistent storage for production
DATASETS: Dict[str, dict] = {
    "demo-dataset": {
        "id": "demo-dataset",
        "file_name": "demo.csv",
        "goldens": [
            {"id": "demo-1", "input": "What is the capital of France?", "expected_output": "Paris", "context": []},
            {"id": "demo-2", "input": "Name a primary color", "expected_output": "Blue", "context": []},
        ],
    }
}


class DatasetUploadResponse(BaseModel):
    dataset_id: str
    file_name: str


@router.post("/upload", response_model=DatasetUploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    ext = (file.filename or "").split(".")[-1].lower()
    if ext not in {"pdf", "md", "txt", "csv"}:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    dataset_id = str(uuid.uuid4())
    dest_path = DATA_DIR / f"{dataset_id}.{ext}"
    with dest_path.open("wb") as f:
        f.write(await file.read())

    # Build a minimal dataset representation. In a real app this would hydrate
    # deepeval EvaluationDataset objects, but here we keep a lightweight shape
    # to avoid heavyweight runtime dependencies.
    if ext == "csv":
        df = pd.read_csv(dest_path)
        goldens = [
            {
                "input": row.get("input") or row.get("question") or "",
                "expected_output": row.get("expected_output") or row.get("answer"),
                "context": [],
            }
            for _, row in df.iterrows()
        ]
    else:
        # For non-CSV inputs, keep a placeholder golden so downstream nodes have data
        goldens = [
            {
                "input": f"Document from {file.filename}",
                "expected_output": None,
                "context": [],
            }
        ]

    DATASETS[dataset_id] = {"id": dataset_id, "file_name": file.filename, "file_path": str(dest_path), "goldens": goldens}

    return DatasetUploadResponse(dataset_id=dataset_id, file_name=file.filename)


@router.get("/{dataset_id}/goldens.csv")
def download_goldens_csv(dataset_id: str):
    dataset = DATASETS.get(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    goldens = dataset.get("goldens") or []
    if not goldens:
        raise HTTPException(status_code=400, detail="Dataset has no golden rows to export")

    csv_path = DATA_DIR / f"{dataset_id}_goldens.csv"
    df = pd.DataFrame(goldens)
    df.to_csv(csv_path, index=False)

    return FileResponse(
        path=csv_path,
        media_type="text/csv",
        filename=f"{dataset_id}_goldens.csv",
    )


@router.get("/{dataset_id}/export/goldens.json")
def download_goldens_json(dataset_id: str):
    """Export goldens as JSON for DeepEval."""
    dataset = DATASETS.get(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    goldens = dataset.get("goldens") or []
    if not goldens:
        raise HTTPException(
            status_code=400,
            detail="Dataset has no golden rows to export"
        )

    # Format goldens for DeepEval
    json_data = {
        "dataset_id": dataset_id,
        "file_name": dataset.get("file_name"),
        "total_goldens": len(goldens),
        "goldens": goldens,
        "exported_at": pd.Timestamp.now().isoformat(),
        "format": "deepeval"
    }

    import json
    json_path = DATA_DIR / f"{dataset_id}_goldens.json"
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    return FileResponse(
        path=json_path,
        media_type="application/json",
        filename=f"{dataset_id}_goldens_deepeval.json",
    )
