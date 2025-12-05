import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from fastapi.testclient import TestClient

# Ensure repository root is importable so `backend` can be resolved when the tests
# are run from the project root.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(REPO_ROOT))

import backend.actions_deepeval as actions_deepeval
import backend.datasets as datasets
from backend.datasets import DATA_DIR
from backend.main import app
from backend.models import FlowEdge, FlowExecutionRequest, FlowNode, FlowNodeData, NodeType
from jose import jwt


client = TestClient(app)
WORKSPACE_ID = "ws-ground-truth"


def _issue_token(user_id: str = "test-user", workspace_roles: List[dict] | None = None, is_admin: bool = False) -> str:
    secret = os.getenv("SUPABASE_JWT_SECRET", "dev-insecure-secret")
    payload = {
        "sub": user_id,
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "workspace_roles": workspace_roles
        if workspace_roles is not None
        else [
            {"workspace_id": WORKSPACE_ID, "group_id": "grp-ops", "role": "workspace_admin"}
        ],
    }
    if is_admin:
        payload["role"] = "service_role"
    return jwt.encode(payload, secret, algorithm="HS256")


client.headers.update(
    {
        "Authorization": f"Bearer {_issue_token()}",
        "X-Workspace-Id": WORKSPACE_ID,
    }
)


def _build_flow_request(nodes: List[FlowNode], edges: List[FlowEdge]) -> Dict:
    request = FlowExecutionRequest(nodes=nodes, edges=edges)
    return request.model_dump(mode="json")


def test_action_catalog_includes_flowbuilder_actions():
    response = client.get(f"/node-types/{NodeType.DATASET_SELECTOR.value}/actions")
    assert response.status_code == 200

    action_ids = {action["id"] for action in response.json()}
    assert "dataset.load" in action_ids

    response = client.get(f"/node-types/{NodeType.FILE_UPLOAD.value}/actions")
    assert response.status_code == 200
    assert "dataset.upload" in {action["id"] for action in response.json()}


def test_upload_dataset_and_execute_flow(tmp_path: Path):
    dataset_path = tmp_path / "goldens.csv"
    dataset_path.write_text("input,expected_output\nWhat?,This\nWho?,That\n")

    with dataset_path.open("rb") as file_handle:
        response = client.post(
            "/datasets/upload",
            files={"file": (dataset_path.name, file_handle, "text/csv")},
        )

    assert response.status_code == 200
    payload = response.json()
    dataset_id = payload["dataset_id"]
    assert payload["file_name"] == dataset_path.name

    upload_node = FlowNode(
        id="upload",
        type=NodeType.FILE_UPLOAD,
        data=FlowNodeData(
            label="Upload Dataset",
            actionId="dataset.upload",
            params={"dataset_id": dataset_id},
        ),
    )
    load_node = FlowNode(
        id="load",
        type=NodeType.DATASET_SELECTOR,
        data=FlowNodeData(
            label="Load Dataset",
            actionId="dataset.load",
            params={"dataset_id": dataset_id},
        ),
    )

    request_payload = _build_flow_request(
        nodes=[upload_node, load_node],
        edges=[FlowEdge(id="edge-1", source="upload", target="load")],
    )

    response = client.post("/flows/execute", json=request_payload)
    assert response.status_code == 200

    results = response.json()
    assert results["upload"]["status"] == "success"
    assert results["load"]["status"] == "success"
    assert results["load"]["output"]["dataset_id"] == dataset_id
    assert (DATA_DIR / f"{dataset_id}.csv").exists()


def test_deepeval_goldens_are_persisted(tmp_path: Path, monkeypatch):
    temp_registry: Dict[str, dict] = {}
    monkeypatch.setattr(datasets, "DATASETS", temp_registry)
    monkeypatch.setattr(actions_deepeval, "DATASETS", temp_registry)
    monkeypatch.setattr(actions_deepeval, "DATA_DIR", tmp_path)

    synth_node = FlowNode(
        id="synth",
        type=NodeType.DEEPEVAL_SYNTHESIZER,
        data=FlowNodeData(
            label="Synthesize goldens",
            actionId="deepeval.generate_goldens_from_docs",
            params={
                "document_paths": ["/tmp/doc1.pdf", "/tmp/doc2.pdf"],
                "max_goldens_per_context": 1,
                "include_expected_output": True,
            },
        ),
    )

    request_payload = _build_flow_request(nodes=[synth_node], edges=[])
    response = client.post("/flows/execute", json=request_payload)

    assert response.status_code == 200
    payload = response.json()["synth"]["output"]
    dataset_id = payload["dataset_id"]

    assert payload["download_url"].endswith("/goldens.csv")
    assert (tmp_path / f"{dataset_id}_goldens.csv").exists()
    assert datasets.DATASETS[dataset_id]["goldens"]


def test_flow_cycle_is_rejected():
    first = FlowNode(
        id="first",
        type=NodeType.FUNCTION,
        data=FlowNodeData(label="First", actionId=None),
    )
    second = FlowNode(
        id="second",
        type=NodeType.FUNCTION,
        data=FlowNodeData(label="Second", actionId=None),
    )

    request_payload = _build_flow_request(
        nodes=[first, second],
        edges=[FlowEdge(id="e1", source="first", target="second"), FlowEdge(id="e2", source="second", target="first")],
    )

    response = client.post("/flows/execute", json=request_payload)
    assert response.status_code == 400
    assert "Flow contains cycles" in response.json()["detail"]


def test_missing_action_is_reported():
    node = FlowNode(
        id="orphan",
        type=NodeType.FUNCTION,
        data=FlowNodeData(label="Orphan", actionId="nonexistent.action"),
    )

    request_payload = _build_flow_request(nodes=[node], edges=[])
    response = client.post("/flows/execute", json=request_payload)
    assert response.status_code == 200
    assert response.json()["orphan"]["status"] == "error"


def test_new_users_are_given_default_workspace_membership():
    default_workspace_id = os.getenv("DEFAULT_WORKSPACE_ID", "ws-default")

    token = _issue_token(user_id="fresh-user", workspace_roles=[])
    headers = {
        "Authorization": f"Bearer {token}",
        "X-Workspace-Id": default_workspace_id,
    }

    response = client.get("/datasets/demo-dataset/goldens.csv", headers=headers)

    # Users without explicit workspace assignments should inherit the default workspace
    # via auth context so they can access member-guarded routes for that workspace.
    assert response.status_code == 200
