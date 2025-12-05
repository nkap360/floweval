import logging
from typing import Any, Callable, Dict, List

from .models import FlowNode, NodeActionDefinition, NodeExecutionResult, NodeType
# ActionParam, ActionParamType

ActionContext = Dict[str, Any]
ActionHandler = Callable[[FlowNode, ActionContext], NodeExecutionResult]

ACTION_DEFS: Dict[str, NodeActionDefinition] = {}
ACTION_HANDLERS: Dict[str, ActionHandler] = {}

logger = logging.getLogger(__name__)


def register_action(defn: NodeActionDefinition) -> str:
    ACTION_DEFS[defn.id] = defn
    logger.debug(
        "Registered action definition %s for nodeType=%s with %d params",
        defn.id,
        defn.nodeType,
        len(defn.params),
    )
    return defn.id


def register_handler(action_id: str):
    def decorator(fn: ActionHandler):
        ACTION_HANDLERS[action_id] = fn
        logger.debug("Registered handler for action_id=%s", action_id)
        return fn

    return decorator


def get_actions_for_node_type(node_type: NodeType) -> List[NodeActionDefinition]:
    actions = [action for action in ACTION_DEFS.values() if action.nodeType == node_type]
    logger.debug("Resolved %d actions for node type %s", len(actions), node_type)
    return actions
