import logging
from typing import Any, Dict
import pandas as pd
from ..core.actions import register_action, register_handler
from ..services.datasets import DATASETS, DATA_DIR
from ..core.models import ActionParam, ActionParamType, FlowNode, NodeActionDefinition, NodeExecutionResult, NodeType

logger = logging.getLogger(__name__)

LOAD_DATASET_ACTION_ID = register_action(
    NodeActionDefinition(
        id="dataset.load",
        label="Load dataset",
        description="Load an uploaded dataset by ID into the flow context",
        nodeType=NodeType.DATASET_SELECTOR,
        params=[
            ActionParam(
                name="dataset_id",
                label="Dataset ID",
                type=ActionParamType.STRING,
                required=True,
            )
        ],
    )
)


UPLOAD_DATASET_ACTION_ID = register_action(
    NodeActionDefinition(
        id="dataset.upload",
        label="Upload dataset file",
        description="Upload a dataset file and share its ID with downstream nodes",
        nodeType=NodeType.FILE_UPLOAD,
        params=[
            ActionParam(
                name="dataset_file",
                label="Dataset file",
                type=ActionParamType.FILE,
                required=True,
            ),
            ActionParam(
                name="dataset_id",
                label="Dataset ID (auto-filled after upload)",
                type=ActionParamType.STRING,
                required=False,
            ),
        ],
    )
)


GENERATE_GOLDENS_ACTION_ID = register_action(
    NodeActionDefinition(
        id="dataset.generate_goldens",
        label="Generate golden dataset",
        description="Create a synthetic golden dataset from the uploaded file using DeepEval and expose a CSV download link",
        nodeType=NodeType.BACKEND_ACTION,
        params=[
            ActionParam(
                name="dataset_id",
                label="Dataset ID",
                type=ActionParamType.STRING,
                required=False,
            ),
            ActionParam(
                name="max_goldens_per_context",
                label="Max goldens per context",
                type=ActionParamType.NUMBER,
                required=False,
                default=1,
            ),
            ActionParam(
                name="max_contexts_per_document",
                label="Max contexts per document",
                type=ActionParamType.NUMBER,
                required=False,
                default=2,
            ),
            ActionParam(
                name="max_context_length",
                label="Max context length",
                type=ActionParamType.NUMBER,
                required=False,
                default=2,
            ),
            ActionParam(
                name="chunk_size",
                label="Chunk size",
                type=ActionParamType.NUMBER,
                required=False,
                default=512,
            ),
            ActionParam(
                name="chunk_overlap",
                label="Chunk overlap",
                type=ActionParamType.NUMBER,
                required=False,
                default=64,
            ),
            ActionParam(
                name="context_quality_threshold",
                label="Context quality threshold",
                type=ActionParamType.NUMBER,
                required=False,
                default=0.7,
            ),
            ActionParam(
                name="context_similarity_threshold",
                label="Context similarity threshold",
                type=ActionParamType.NUMBER,
                required=False,
                default=0.7,
            ),
            ActionParam(
                name="critic_model",
                label="Critic model",
                type=ActionParamType.STRING,
                required=False,
                default="gpt-4o-mini",
            ),
            ActionParam(
                name="synthesizer_model",
                label="Synthesizer model",
                type=ActionParamType.STRING,
                required=False,
                default="gpt-4o-mini",
            ),
        ],
    )
)


@register_handler(LOAD_DATASET_ACTION_ID)
def load_dataset_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    dataset_id = node.data.params.get("dataset_id")
    if not dataset_id or dataset_id not in DATASETS:
        return NodeExecutionResult(status="error", error=f"Unknown dataset_id={dataset_id}")

    dataset = DATASETS[dataset_id]
    logger.info("Loading dataset into flow context", extra={"dataset_id": dataset_id})
    ctx["dataset_id"] = dataset_id
    ctx["dataset"] = dataset
    return NodeExecutionResult(
        status="success",
        output={"dataset_id": dataset_id, "goldens_count": len(dataset.get("goldens", []))},
    )


@register_handler(UPLOAD_DATASET_ACTION_ID)
def upload_dataset_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    dataset_id = node.data.params.get("dataset_id")
    if not dataset_id:
        return NodeExecutionResult(status="error", error="No dataset_id set. Upload file in the properties panel first.")

    if dataset_id not in DATASETS:
        return NodeExecutionResult(status="error", error=f"Uploaded dataset {dataset_id} not found on server")

    logger.info(
        "Dataset upload metadata acknowledged; sharing dataset in context",
        extra={"dataset_id": dataset_id, "file_name": DATASETS[dataset_id].get("file_name")},
    )
    ctx["dataset_id"] = dataset_id
    ctx["dataset"] = DATASETS[dataset_id]
    return NodeExecutionResult(
        status="success",
        output={"dataset_id": dataset_id, "file_name": DATASETS[dataset_id].get("file_name")},
    )


@register_handler(GENERATE_GOLDENS_ACTION_ID)
def generate_goldens_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    dataset_id = ctx.get("dataset_id") or node.data.params.get("dataset_id")
    if not dataset_id:
        return NodeExecutionResult(status="error", error="No dataset in context. Upload or load one first.")

    dataset = DATASETS.get(dataset_id)
    if not dataset:
        return NodeExecutionResult(status="error", error=f"Dataset {dataset_id} not found")

    file_path = dataset.get("file_path")
    if not file_path:
        return NodeExecutionResult(status="error", error=f"No file path found for dataset {dataset_id}")

    # Extract parameters with defaults
    max_goldens_per_context = int(node.data.params.get("max_goldens_per_context", 1))
    max_contexts_per_document = int(node.data.params.get("max_contexts_per_document", 2))
    max_context_length = int(node.data.params.get("max_context_length", 2))
    chunk_size = int(node.data.params.get("chunk_size", 512))
    chunk_overlap = int(node.data.params.get("chunk_overlap", 64))
    context_quality_threshold = float(node.data.params.get("context_quality_threshold", 0.7))
    context_similarity_threshold = float(node.data.params.get("context_similarity_threshold", 0.7))
    critic_model = node.data.params.get("critic_model", "gpt-4o-mini")
    synthesizer_model = node.data.params.get("synthesizer_model", "gpt-4o-mini")

    file_name = dataset.get("file_name", "uploaded document")

    logger.info(
        "Generating goldens from document using my_module",
        extra={
            "dataset_id": dataset_id,
            "file_path": file_path,
            "max_goldens_per_context": max_goldens_per_context,
            "max_contexts_per_document": max_contexts_per_document,
            "critic_model": critic_model,
            "synthesizer_model": synthesizer_model
        }
    )

    try:
        # Import from modules to avoid circular imports
        from ..modules import generate_goldens_from_documents

        # Call the enhanced golden generation function
        result = generate_goldens_from_documents(
            document_paths=file_path,
            max_goldens_per_context=max_goldens_per_context,
            max_contexts_per_document=max_contexts_per_document,
            max_context_length=max_context_length,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            context_quality_threshold=context_quality_threshold,
            context_similarity_threshold=context_similarity_threshold,
            critic_model=critic_model,
            synthesizer_model=synthesizer_model,
        )

        goldens = result["goldens"]
        summary = result["summary"]

        # Convert goldens to DataFrame and save
        goldens_data = []
        for idx, golden in enumerate(goldens):
            # Debug logging to see the golden structure
            logger.debug(f"Processing golden {idx}: {type(golden)} - {golden}")
            
            # Handle both object and dictionary formats
            if isinstance(golden, dict):
                golden_dict = {
                    "id": golden.get("id", f"{dataset_id}-golden-{idx + 1}"),
                    "input": golden.get("input", ""),
                    "expected_output": golden.get("expected_output", ""),
                    "context": golden.get("context", ""),
                }
            else:
                # Handle object format - try different attribute access patterns
                # DeepEval Golden objects have specific attributes
                input_val = ""
                expected_output_val = ""
                context_val = ""
                
                # Try direct attribute access
                try:
                    input_val = str(golden.input) if hasattr(golden, 'input') else ""
                    expected_output_val = str(golden.expected_output) if hasattr(golden, 'expected_output') else ""
                    context_val = str(golden.context) if hasattr(golden, 'context') else ""
                except Exception as e:
                    logger.warning(f"Error accessing golden attributes: {e}")
                
                # Try alternative attribute names
                if not input_val:
                    input_val = str(getattr(golden, "query", "")) or str(getattr(golden, "question", ""))
                
                golden_dict = {
                    "id": str(getattr(golden, "id", f"{dataset_id}-golden-{idx + 1}")),
                    "input": input_val,
                    "expected_output": expected_output_val,
                    "context": context_val,
                }
            
            # Only add valid goldens with actual input content
            # Skip placeholder entries
            if golden_dict["input"] and not golden_dict["input"].startswith("Document from"):
                goldens_data.append(golden_dict)
                logger.debug(f"Added golden to CSV: {golden_dict['input'][:50]}...")
        
        # Log the goldens data we're about to save
        logger.info(f"Prepared {len(goldens_data)} goldens for CSV export")
        for i, g in enumerate(goldens_data):
            logger.debug(f"CSV Golden {i}: {g['input'][:50]}...")
        
        # Create DataFrame and save to CSV
        csv_path = DATA_DIR / f"{dataset_id}_goldens.csv"
        logger.info(f"Creating DataFrame with {len(goldens_data)} goldens")
        df = pd.DataFrame(goldens_data)
        logger.info(f"DataFrame shape: {df.shape}")
        logger.info(f"DataFrame columns: {df.columns.tolist()}")
        logger.info(f"Saving to CSV: {csv_path}")
        
        # Ensure directory exists
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to CSV
        df.to_csv(csv_path, index=False)
        logger.info(f"CSV saved successfully to {csv_path}")
        
        # Verify the file was written correctly
        if csv_path.exists():
            file_size = csv_path.stat().st_size
            logger.info(f"CSV file exists, size: {file_size} bytes")
            
            # Read back the first few lines to verify content
            with open(csv_path, 'r') as f:
                first_lines = [next(f) for _ in range(min(3, sum(1 for _ in open(csv_path))))]
                logger.info(f"CSV file first lines: {first_lines}")
        else:
            logger.error(f"CSV file was not created at {csv_path}")
        
        # CRITICAL: Update the DATASETS dictionary with the actual goldens
        # This ensures the download endpoint serves the correct data
        # Use the module-level DATASETS import (already imported at top of file)
        if dataset_id in DATASETS:
            logger.info(f"Updating DATASETS[{dataset_id}] with {len(goldens_data)} actual goldens")
            DATASETS[dataset_id]["goldens"] = goldens_data
            logger.info("DATASETS dictionary updated successfully")
        else:
            logger.warning(f"Dataset {dataset_id} not found in DATASETS dictionary")

        download_url = f"/datasets/{dataset_id}/goldens.csv"
        ctx["dataset"] = dataset
        ctx["dataset_id"] = dataset_id
        ctx["goldens_csv"] = str(csv_path)
        ctx["goldens_data"] = goldens_data  # Store for review action

        logger.info(
            "Goldens generated and CSV cached at %s", csv_path,
            extra={
                "dataset_id": dataset_id,
                "total_goldens": summary.total_goldens,
                "with_expected_output": summary.with_expected_output,
                "without_expected_output": summary.without_expected_output
            }
        )

        return NodeExecutionResult(
            status="success",
            output={
                "dataset_id": dataset_id,
                "generated": summary.total_goldens,
                "download_url": download_url,
                "file_name": file_name,
                "summary": {
                    "num_documents": summary.num_documents,
                    "total_goldens": summary.total_goldens,
                    "with_expected_output": summary.with_expected_output,
                    "without_expected_output": summary.without_expected_output,
                }
            },
        )

    except Exception as exc:
        logger.exception("Error generating goldens with my_module", extra={"dataset_id": dataset_id})
        return NodeExecutionResult(status="error", error=f"Failed to generate goldens: {str(exc)}")


# Register Review Goldens Action
REVIEW_GOLDENS_ACTION_ID = register_action(
    NodeActionDefinition(
        id="dataset.review_goldens",
        label="Review Goldens",
        description="Open review interface for human validation of generated goldens",
        nodeType=NodeType.BACKEND_ACTION,
        params=[
            ActionParam(
                name="dataset_id",
                label="Dataset ID",
                type=ActionParamType.STRING,
                required=True,
            ),
        ],
    )
)


@register_handler(REVIEW_GOLDENS_ACTION_ID)
def review_goldens_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    """
    Trigger the golden review workflow.
    This action signals the frontend to open the review page.
    """
    dataset_id = node.data.params.get("dataset_id") or ctx.get("dataset_id")
    
    if not dataset_id:
        return NodeExecutionResult(status="error", error="No dataset_id provided")
    
    # Generate session ID
    import time
    import random
    import string
    session_id = f"session-{int(time.time())}-{''.join(random.choices(string.ascii_lowercase + string.digits, k=9))}"
    
    # Get goldens from context (generated by previous node)
    goldens_data = ctx.get("goldens_data", [])
    
    if not goldens_data:
        # Try to load from CSV if available
        csv_path = ctx.get("goldens_csv")
        if csv_path:
            import pandas as pd
            from pathlib import Path
            import json
            import ast
            df = pd.read_csv(Path(csv_path))
            goldens_data = df.to_dict('records')
            
            # Parse context field if it's a string representation of a list
            for golden in goldens_data:
                if 'context' in golden and isinstance(golden['context'], str):
                    try:
                        # Try JSON parse first
                        golden['context'] = json.loads(golden['context'])
                    except (json.JSONDecodeError, ValueError):
                        try:
                            # Try ast.literal_eval for Python string representation
                            golden['context'] = ast.literal_eval(golden['context'])
                        except (ValueError, SyntaxError):
                            # If all parsing fails, wrap in array
                            golden['context'] = [golden['context']] if golden['context'] else []
                    
                    # Ensure it's a list
                    if not isinstance(golden['context'], list):
                        golden['context'] = [str(golden['context'])]
    
    logger.info(
        "Review goldens action triggered",
        extra={
            "dataset_id": dataset_id,
            "session_id": session_id,
            "goldens_count": len(goldens_data)
        }
    )
    
    # Store in context for frontend to pick up
    ctx["review_session_id"] = session_id
    ctx["review_dataset_id"] = dataset_id
    ctx["review_goldens"] = goldens_data
    
    # Return special action type that frontend recognizes
    review_url = (
        f"/datasets/{dataset_id}/review-goldens"
        f"?session={session_id}&returnTo=/flow-builder"
    )
    
    return NodeExecutionResult(
        status="pending",
        output={
            "action_type": "navigate_to_review",
            "dataset_id": dataset_id,
            "session_id": session_id,
            "goldens": goldens_data,
            "goldens_count": len(goldens_data),
            "review_url": review_url,
            "message": f"Review {len(goldens_data)} golden(s) before continuing"
        },
        meta={
            "requires_user_action": True,
            "action_type": "navigate_to_review"
        }
    )


# Export Goldens Action
EXPORT_GOLDENS_ACTION_ID = register_action(
    NodeActionDefinition(
        id="dataset.export_goldens",
        label="Export Goldens",
        description="Export reviewed goldens as JSON for DeepEval",
        nodeType=NodeType.BACKEND_ACTION,
        params=[
            ActionParam(
                name="dataset_id",
                label="Dataset ID",
                type=ActionParamType.STRING,
                required=False,
            ),
        ],
    )
)


@register_handler(EXPORT_GOLDENS_ACTION_ID)
def export_goldens_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    """
    Export reviewed goldens as downloadable JSON.
    Retrieves goldens from context (after review) and generates download link.
    """
    dataset_id = node.data.params.get("dataset_id") or ctx.get("dataset_id")
    
    logger.info(
        "Export goldens action started",
        extra={
            "dataset_id": dataset_id,
            "context_keys": list(ctx.keys()),
            "has_reviewed_goldens": "reviewed_goldens" in ctx,
            "has_goldens_data": "goldens_data" in ctx
        }
    )
    
    if not dataset_id:
        return NodeExecutionResult(status="error", error="No dataset_id provided")
    
    # Get reviewed goldens from context
    reviewed_goldens = ctx.get("reviewed_goldens") or ctx.get("goldens_data", [])
    
    if not reviewed_goldens:
        # Try to load from CSV if available
        csv_path = ctx.get("goldens_csv")
        if csv_path:
            import pandas as pd
            from pathlib import Path
            try:
                df = pd.read_csv(Path(csv_path))
                reviewed_goldens = df.to_dict('records')
            except Exception as e:
                logger.error(f"Failed to load goldens from CSV: {e}")
    
    if not reviewed_goldens:
        return NodeExecutionResult(
            status="error",
            error="No goldens found to export. Please generate or review goldens first."
        )
    
    # Generate download URL
    download_url = f"/datasets/{dataset_id}/export/goldens.json"
    
    logger.info(
        "Export goldens action completed",
        extra={
            "dataset_id": dataset_id,
            "goldens_count": len(reviewed_goldens)
        }
    )
    
    # Store exported goldens in context
    ctx["exported_goldens"] = reviewed_goldens
    
    result_output = {
        "dataset_id": dataset_id,
        "goldens_count": len(reviewed_goldens),
        "download_url": download_url,
        "message": f"Successfully exported {len(reviewed_goldens)} golden(s)",
        "format": "JSON",
        "ready_for_deepeval": True
    }
    
    logger.info(
        "Export goldens action - Returning result",
        extra={
            "status": "success",
            "output_keys": list(result_output.keys()),
            "download_url": download_url,
            "goldens_count": len(reviewed_goldens)
        }
    )
    
    return NodeExecutionResult(
        status="success",
        output=result_output
    )
