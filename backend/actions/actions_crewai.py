import logging
from typing import Any, Dict

from ..core.actions import register_action, register_handler
from ..crew.lead_score_flow import run_lead_score_flow
from ..core.models import ActionParam, ActionParamType, FlowNode, NodeActionDefinition, NodeExecutionResult, NodeType

logger = logging.getLogger(__name__)

RUN_LEAD_SCORE_FLOW_ID = register_action(
    NodeActionDefinition(
        id="crewai.run_lead_score_flow",
        label="Run CrewAI Lead Score Flow",
        description="Scores leads via a CrewAI Flow",
        nodeType=NodeType.CREWAI_FLOW,
        params=[
            ActionParam(
                name="leads_dataset_id",
                label="Leads dataset ID",
                type=ActionParamType.STRING,
                required=True,
            ),
            ActionParam(
                name="max_leads",
                label="Max leads to score",
                type=ActionParamType.NUMBER,
                required=False,
                default=50,
            ),
        ],
    )
)


@register_handler(RUN_LEAD_SCORE_FLOW_ID)
def run_lead_score_action(node: FlowNode, ctx: Dict[str, Any]) -> NodeExecutionResult:
    dataset_id = node.data.params.get("leads_dataset_id")
    if not dataset_id:
        return NodeExecutionResult(status="error", error="Missing leads_dataset_id param")

    csv_path = f"data/{dataset_id}.csv"
    max_leads = int(node.data.params.get("max_leads", 50))
    logger.info(
        "Starting CrewAI lead score flow", extra={"dataset_id": dataset_id, "csv_path": csv_path, "max_leads": max_leads}
    )
    result = run_lead_score_flow(csv_path, max_leads=max_leads)
    ctx["lead_scores"] = result

    logger.debug("CrewAI lead scoring completed", extra={"dataset_id": dataset_id, "scored": len(result)})

    return NodeExecutionResult(status="success", output=result)
