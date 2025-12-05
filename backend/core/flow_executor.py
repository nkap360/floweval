import logging
from typing import Any, Dict, List
from fastapi import APIRouter, Depends, HTTPException
from .actions import ACTION_HANDLERS
from ..services.auth import require_user
from .models import FlowEdge, FlowExecutionRequest, FlowNode, NodeExecutionResult


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/flows", tags=["flows"], dependencies=[Depends(require_user())])


def topo_sort(nodes: List[FlowNode], edges: List[FlowEdge]) -> List[FlowNode]:
    id_to_node = {node.id: node for node in nodes}
    incoming: Dict[str, int] = {node.id: 0 for node in nodes}
    adjacency: Dict[str, List[str]] = {node.id: [] for node in nodes}

    for edge in edges:
        adjacency[edge.source].append(edge.target)
        incoming[edge.target] += 1

    queue = [node_id for node_id, degree in incoming.items() if degree == 0]
    ordered: List[str] = []

    while queue:
        node_id = queue.pop(0)
        ordered.append(node_id)
        for target in adjacency[node_id]:
            incoming[target] -= 1
            if incoming[target] == 0:
                queue.append(target)

    if len(ordered) != len(nodes):
        raise HTTPException(status_code=400, detail="Flow contains cycles")

    return [id_to_node[node_id] for node_id in ordered]


@router.post("/execute")
def execute_flow(request: FlowExecutionRequest) -> Dict[str, NodeExecutionResult]:
    logger.info("=" * 80)
    logger.info("FLOW EXECUTION STARTED")
    logger.info("=" * 80)
    logger.info(
        "Flow execution - Request details: nodes=%d, edges=%d, has_context=%s",
        len(request.nodes),
        len(request.edges),
        request.context is not None
    )
    
    if request.context:
        logger.info(
            "Flow execution - Initial context keys: %s",
            list(request.context.keys())
        )
        logger.info(
            "Flow execution - Context types: %s",
            {k: type(v).__name__ for k, v in request.context.items()}
        )
    
    results: Dict[str, NodeExecutionResult] = {}
    # Use initial context if provided
    context: Dict[str, Any] = request.context or {}

    try:
        ordered_nodes = topo_sort(request.nodes, request.edges)
        logger.info(
            "Flow execution - Topological order determined: [%s]",
            ", ".join(f"{node.id}({node.data.actionId or 'no-action'})" for node in ordered_nodes)
        )
    except Exception as e:
        logger.error("Flow execution - Topological sort failed: %s", str(e))
        raise
    
    for idx, node in enumerate(ordered_nodes, 1):
        logger.info("-" * 80)
        logger.info("EXECUTING NODE %d/%d: %s", idx, len(ordered_nodes), node.id)
        logger.info("-" * 80)
        
        action_id = node.data.actionId
        if not action_id:
            logger.info("Node %s - No action configured, marking as skipped", node.id)
            results[node.id] = NodeExecutionResult(status="success", output={"skipped": True})
            continue

        handler = ACTION_HANDLERS.get(action_id)
        if not handler:
            logger.error("Node %s - No handler registered for action_id=%s", node.id, action_id)
            results[node.id] = NodeExecutionResult(status="error", error=f"No handler for action {action_id}")
            continue

        try:
            logger.info("Node %s - Executing action: %s", node.id, action_id)
            logger.info("Node %s - Input params: %s", node.id, node.data.params)
            logger.info("Node %s - Context available: %s", node.id, list(context.keys()))
            
            result = handler(node, context)
            
            logger.info("Node %s - Execution completed with status: %s", node.id, result.status)
            if result.output:
                logger.info("Node %s - Output keys: %s", node.id, list(result.output.keys()))
            if result.error:
                logger.error("Node %s - Error: %s", node.id, result.error)
                
        except Exception as exc:  # pragma: no cover - safety net for unexpected runtime errors
            logger.exception("Node %s - Unhandled exception during execution", node.id)
            result = NodeExecutionResult(status="error", error=str(exc))

        results[node.id] = result
        
        # Check if this action requires user interaction (e.g., review)
        if result.meta and result.meta.get("requires_user_action"):
            action_type = result.meta.get("action_type")
            logger.info("=" * 80)
            logger.info("FLOW PAUSED - User action required: %s", action_type)
            logger.info("Node %s triggered pause", node.id)
            logger.info("Completed %d/%d nodes before pause", idx, len(ordered_nodes))
            logger.info("=" * 80)
            # Return results up to this point - remaining nodes won't execute
            return results

    logger.info("=" * 80)
    logger.info("FLOW EXECUTION COMPLETED - All %d nodes executed", len(ordered_nodes))
    logger.info("=" * 80)
    return results
