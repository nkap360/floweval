import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

import pandas as pd

from ..core.actions import register_action, register_handler
from ..services.datasets import DATASETS, DATA_DIR
from ..core.models import ActionParam, ActionParamType, FlowNode, NodeActionDefinition, NodeExecutionResult, NodeType


logger = logging.getLogger(__name__)

RUN_EVAL_ACTION_ID = register_action(
    NodeActionDefinition(
        id="deepeval.run_eval",
        label="Run Deepeval Metrics",
        description="Run evaluation metrics on the dataset in context",
        nodeType=NodeType.DEEPEVAL,
        params=[
            ActionParam(
                name="model_target",
                label="Model name",
                type=ActionParamType.STRING,
                required=True,
                default="gpt-4o-mini",
            ),
        ],
    )
)


GENERATE_GOLDENS_FROM_DOCS_ACTION_ID = register_action(
    NodeActionDefinition(
        id="deepeval.generate_goldens_from_docs",
        label="Generate goldens from documents",
        description="Simulate deepeval Synthesizer.generate_goldens_from_docs with context construction controls",
        nodeType=NodeType.DEEPEVAL_SYNTHESIZER,
        params=[
            ActionParam(
                name="document_paths",
                label="Document paths (JSON list)",
                type=ActionParamType.JSON,
                required=True,
                default=["example.txt", "example.pdf"],
            ),
            ActionParam(
                name="include_expected_output",
                label="Include expected output",
                type=ActionParamType.BOOLEAN,
                required=False,
                default=True,
            ),
            ActionParam(
                name="max_goldens_per_context",
                label="Max goldens per context",
                type=ActionParamType.NUMBER,
                required=False,
                default=2,
            ),
            ActionParam(
                name="context_construction_config",
                label="Context construction config (JSON)",
                type=ActionParamType.JSON,
                required=False,
                default={
                    "max_contexts_per_document": 3,
                    "max_context_length": 3,
                    "chunk_size": 1024,
                    "context_quality_threshold": 0.5,
                },
            ),
        ],
    )
)


def _score_value(seed: int) -> float:
    # deterministic pseudo score between 0.6 and 1.0
    return 0.6 + (hash(seed) % 400) / 1000


def _call_llm(model_name: str, prompt: str) -> str:
    return f"[{model_name}] Answer to: {prompt}"


def _parse_json(value: Any, fallback: Any) -> Any:
    if value is None:
        return fallback
    if isinstance(value, (list, dict)):
        return value
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return fallback
    return fallback


def _coerce_bool(value: Any, default: bool) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y"}
    return default


@register_handler(RUN_EVAL_ACTION_ID)
def run_deepeval_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    dataset = ctx.get("dataset")
    if not dataset:
        logger.warning("deepeval.run_eval called without dataset in context")
        return NodeExecutionResult(
            status="error",
            error="No dataset in context. Ensure dataset.upload or dataset.load ran before deepeval.run_eval.",
        )

    goldens: List[Dict[str, Any]] = dataset.get("goldens", [])
    model_target = node.data.params.get("model_target", "gpt-4o-mini")

    logger.info(
        "Running deepeval metrics for dataset_id=%s with %d goldens using model=%s",
        ctx.get("dataset_id"),
        len(goldens),
        model_target,
    )

    results = []
    passed = 0
    for idx, golden in enumerate(goldens or [{}]):
        score = round(_score_value(idx), 2)
        tc_passed = score >= 0.8
        passed += 1 if tc_passed else 0
        logger.info(
            "Evaluated item=%s score=%.2f passed=%s", golden.get("id", idx), score, tc_passed
        )
        results.append(
            {
                "item_id": golden.get("id") or f"test_case_{idx}",
                "overall_score": score,
                "passed": tc_passed,
                "generated_answer": _call_llm(model_target, golden.get("input", "")),
            }
        )

    total = len(results) or 1
    summary = {
        "overall_score": round(sum(r["overall_score"] for r in results) / total, 2),
        "pass_rate": round(passed * 100 / total, 2),
        "critical_failures": total - passed,
        "execution_time_ms": 0,
    }

    evaluation_payload = {
        "summary": summary,
        "results": results,
        "total_items": total,
        "dataset_id": ctx.get("dataset_id"),
        "model_target": model_target,
    }

    ctx["evaluation"] = evaluation_payload

    return NodeExecutionResult(status="success", output=evaluation_payload)


@register_handler(GENERATE_GOLDENS_FROM_DOCS_ACTION_ID)
def generate_goldens_from_docs_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    params = node.data.params
    document_paths = _parse_json(params.get("document_paths"), [])
    include_expected_output = _coerce_bool(params.get("include_expected_output"), True)
    max_goldens_per_context = int(params.get("max_goldens_per_context", 2))
    context_config = _parse_json(params.get("context_construction_config"), {})

    if not document_paths:
        return NodeExecutionResult(status="error", error="Provide at least one document path to synthesize goldens.")

    dataset_id = ctx.get("dataset_id") or f"docs-{uuid4().hex[:8]}"
    contexts_per_document = max(1, int(context_config.get("max_contexts_per_document", 3)))
    context_length = max(1, int(context_config.get("max_context_length", 3)))

    goldens: List[Dict[str, Any]] = []
    context_summaries: List[Dict[str, Any]] = []

    logger.info(
        "Synthesizing deepeval goldens from documents",
        extra={
            "dataset_id": dataset_id,
            "documents": len(document_paths),
            "contexts_per_document": contexts_per_document,
            "max_goldens_per_context": max_goldens_per_context,
        },
    )

    for doc_idx, doc in enumerate(document_paths):
        doc_name = Path(str(doc)).name or f"document-{doc_idx + 1}"
        for ctx_idx in range(contexts_per_document):
            snippet = f"Context {ctx_idx + 1} from {doc_name} (chunk span {ctx_idx + 1}-{ctx_idx + context_length})"
            context_summaries.append({"document": doc_name, "context": snippet})

            for golden_idx in range(max_goldens_per_context):
                entry_id = f"{dataset_id}-{doc_idx + 1}-{ctx_idx + 1}-{golden_idx + 1}"
                golden_row = {
                    "id": entry_id,
                    "input": f"Question {golden_idx + 1} grounded in {doc_name} context {ctx_idx + 1}",
                    "context": [snippet],
                }

                if include_expected_output:
                    golden_row["expected_output"] = (
                        f"Answer synthesized from {doc_name} context {ctx_idx + 1} respecting construction config"
                    )

                goldens.append(golden_row)

    file_name = f"{Path(str(document_paths[0])).name if document_paths else 'documents'} (deepeval)"
    goldens_csv = DATA_DIR / f"{dataset_id}_goldens.csv"
    pd.DataFrame(goldens).to_csv(goldens_csv, index=False)

    synthesized_dataset = {
        "id": dataset_id,
        "dataset_id": dataset_id,
        "file_name": file_name,
        "documents": document_paths,
        "goldens": goldens,
        "context_construction_config": context_config,
    }

    DATASETS[dataset_id] = synthesized_dataset

    download_url = f"/datasets/{dataset_id}/goldens.csv"

    ctx["dataset_id"] = dataset_id
    ctx["dataset"] = synthesized_dataset
    ctx["goldens_csv"] = str(goldens_csv)

    logger.info(
        "Generated %d goldens from %d documents using deepeval.generate_goldens_from_docs", len(goldens), len(document_paths)
    )

    return NodeExecutionResult(
        status="success",
        output={
            "dataset_id": dataset_id,
            "documents": document_paths,
            "generated": len(goldens),
            "contexts_created": len(context_summaries),
            "context_examples": context_summaries[:5],
            "include_expected_output": include_expected_output,
            "max_goldens_per_context": max_goldens_per_context,
            "context_construction_config": context_config,
            "download_url": download_url,
            "goldens_csv": str(goldens_csv),
        },
    )
