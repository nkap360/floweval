from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class NodeType(str, Enum):
    MANUAL_TRIGGER = "MANUAL_TRIGGER"
    SET = "SET"
    POSTGRES = "POSTGRES"
    FUNCTION = "FUNCTION"
    DATASET_SELECTOR = "DATASET_SELECTOR"
    DEEPEVAL = "DEEPEVAL"
    BACKEND_ACTION = "BACKEND_ACTION"
    FILE_UPLOAD = "FILE_UPLOAD"
    CREWAI_FLOW = "CREWAI_FLOW"
    DEEPEVAL_SYNTHESIZER = "DEEPEVAL_SYNTHESIZER"


class ActionParamType(str, Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SELECT = "select"
    FILE = "file"
    JSON = "json"


class ActionParam(BaseModel):
    name: str
    label: str
    type: ActionParamType
    required: bool = True
    options: Optional[List[str]] = None
    default: Optional[Any] = None


class NodeActionDefinition(BaseModel):
    id: str
    label: str
    description: Optional[str]
    nodeType: NodeType
    params: List[ActionParam]


class FlowNodeData(BaseModel):
    label: str
    subtitle: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)
    actionId: Optional[str] = None
    params: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class FlowNode(BaseModel):
    id: str
    type: NodeType
    data: FlowNodeData

    # React Flow positioning metadata is ignored by the executor but preserved for clients.
    position: Optional[Dict[str, Any]] = None
    positionAbsolute: Optional[Dict[str, Any]] = None
    width: Optional[float] = None
    height: Optional[float] = None

    class Config:
        extra = "allow"


class FlowEdge(BaseModel):
    id: str
    source: str
    target: str

    # Allow styling metadata to flow through untouched.
    style: Dict[str, Any] = Field(default_factory=dict)
    animated: Optional[bool] = None

    class Config:
        extra = "allow"


class FlowExecutionRequest(BaseModel):
    nodes: List[FlowNode]
    edges: List[FlowEdge]
    context: Optional[Dict[str, Any]] = None  # Initial context for flow


class NodeExecutionResult(BaseModel):
    status: str
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    meta: Dict[str, Any] = Field(default_factory=dict)


FlowExecutionResponse = Dict[str, NodeExecutionResult]
