"""
Core Module
===========
Core components of the Flow Builder engine.

Contains:
- Model definitions (nodes, edges, execution results)
- Action registry and handler system
- Flow execution engine
"""

from .models import *
from .actions import *
from .flow_executor import execute_flow

__all__ = [
    # Models
    "NodeType",
    "ActionParamType",
    "ActionParam",
    "NodeActionDefinition",
    "FlowNodeData",
    "FlowNode",
    "FlowEdge",
    "FlowExecutionRequest",
    "NodeExecutionResult",
    "FlowExecutionResponse",
    # Actions
    "ACTION_DEFS",
    "ACTION_HANDLERS",
    "register_action",
    "register_handler",
    "get_actions_for_node_type",
    # Executor
    "execute_flow",
]
