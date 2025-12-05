# Architecture Guide

Flow Builder is built with a modern, scalable architecture that separates concerns into distinct layers while maintaining clean integration points. This guide provides an overview of the system design and component relationships.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + TypeScript)             │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │ Flow Builder│  │ Annotation  │  │  Chatbot UI     │   │
│  │   (Editor)  │  │   Studio    │  │ (Multi-space)   │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐   │
│  │ Dataset Mgmt│  │   Settings  │  │   Dashboard     │   │
│  │   (CRUD)    │  │ (Config)    │  │  (Analytics)    │   │
│  └─────────────┘  └─────────────┘  └──────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API (HTTPS)
┌────────────────────────┴────────────────────────────────────┐
│                   Backend (FastAPI + Python)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                 API Layer                             │  │
│  │  • CORS Middleware  • Rate Limiting  • Auth          │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Core Engine                               │  │
│  │  • Flow Executor  • Action Registry  • Node Models   │  │
│  │  • Graph Traversal  • Context Management            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Services Layer                           │  │
│  │  • Auth Service   • Dataset Service   • Log Service  │  │
│  │  • Template Service  • Storage Service               │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Actions Layer                            │  │
│  │  • Dataset Actions  • DeepEval  • CrewAI Flows       │  │
│  │  • PDF Processing   • AI Generation                 │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────┐
│          External Services              │
│  ┌─────────────┐  ┌─────────────────┐ │
│  │ Supabase    │  │   AI Providers  │ │
│  │ (Database)  │  │ (Gemini, OpenAI)│ │
│  └─────────────┘  └─────────────────┘ │
│  ┌─────────────┐  ┌─────────────────┐ │
│  │ PDF.js      │  │  Storage        │ │
│  │ (Processing)│  │  (File System)  │ │
│  └─────────────┘  └─────────────────┘ │
└─────────────────────────────────────────┘
```

## 🎯 Design Principles

### 1. Separation of Concerns

- **Frontend**: UI/UX, user interactions, client-side logic
- **Backend API**: HTTP interface, authentication, request handling
- **Core Engine**: Business logic, flow execution, action management
- **Services**: Data access, external integrations, utilities
- **Actions**: Specific operations that can be composed into flows

### 2. Modularity

- **Loose Coupling**: Components communicate through well-defined interfaces
- **High Cohesion**: Related functionality grouped together
- **Extensibility**: Easy to add new actions and providers
- **Testability**: Each layer can be tested independently

### 3. Scalability

- **Stateless API**: Backend can be horizontally scaled
- **Asynchronous Operations**: Long-running operations handled efficiently
- **Resource Management**: Proper cleanup and memory management
- **Caching**: Strategic caching for performance

## 📁 Frontend Architecture

### Technology Stack

- **React 18**: UI framework with hooks and concurrent features
- **TypeScript**: Type safety and developer productivity
- **Vite**: Fast build tool with HMR
- **TailwindCSS**: Utility-first CSS framework
- **React Flow**: Node-based visual editor
- **Supabase Auth**: Authentication and user management

### Directory Structure

```
src/
├── components/           # Reusable UI components
│   ├── Layout.tsx           # App layout wrapper
│   ├── Navigation.tsx       # Top navigation bar
│   ├── LogConsole.tsx       # Log viewer component
│   ├── flow/                # Flow builder components
│   │   ├── CustomNode.tsx      # Node rendering
│   │   ├── FlowSidebar.tsx     # Node palette
│   │   └── PropertiesPanel.tsx # Node configuration
│   └── ui/                  # Base UI components
│       ├── Badge.tsx
│       ├── Button.tsx
│       └── DeleteButton.tsx
├── pages/                # Page-level components
│   ├── FlowBuilder.tsx      # Flow editor page
│   ├── AnnotationStudio.tsx # Document annotation
│   ├── DatasetView.tsx      # Dataset management
│   ├── Dashboard.tsx        # Analytics dashboard
│   ├── Chatbot.tsx          # AI assistant
│   └── Settings.tsx         # User settings
├── services/             # API clients & utilities
│   ├── apiClient.ts         # Base API client
│   ├── actionApi.ts         # Actions API
│   ├── aiService.ts         # AI integration
│   ├── authService.ts       # Authentication
│   └── datasetService.ts    # Dataset operations
├── utils/                # Utility functions
│   └── logger.ts            # Frontend logging
├── App.tsx               # Root component
├── index.tsx             # App entry point
├── types.ts              # TypeScript type definitions
└── index.css             # Global styles
```

### Key Frontend Patterns

#### Service Layer Pattern

```typescript
// services/datasetService.ts
export class DatasetService {
  async getDatasets(): Promise<Dataset[]> {
    // API call to backend
  }

  async createDataset(dataset: CreateDatasetRequest): Promise<Dataset> {
    // API call with error handling
  }
}
```

#### Component Composition

```typescript
// components/flow/FlowBuilder.tsx
export const FlowBuilder: React.FC = () => {
  const [nodes, setNodes] = useState<FlowNode[]>([]);
  const [edges, setEdges] = useState<FlowEdge[]>([]);

  return (
    <div className="flex h-screen">
      <FlowSidebar />
      <FlowCanvas />
      <PropertiesPanel />
    </div>
  );
};
```

## 🖥️ Backend Architecture

### Technology Stack

- **FastAPI**: Modern Python web framework
- **Python 3.9+**: Core language with type hints
- **CrewAI**: Multi-agent AI orchestration
- **DeepEval**: Evaluation metrics and synthesis
- **Supabase**: Database and authentication
- **Pydantic**: Data validation and serialization

### Backend Directory Structure

```
backend/
├── actions/              # Action implementations
│   ├── __init__.py
│   ├── actions_crewai.py    # CrewAI workflow actions
│   ├── actions_dataset.py   # Dataset CRUD operations
│   └── actions_deepeval.py  # Evaluation actions
├── core/                 # Core engine components
│   ├── __init__.py
│   ├── models.py            # Data models (NodeType, FlowNode)
│   ├── actions.py           # Action registry & definitions
│   └── flow_executor.py     # Flow execution engine
├── services/             # Application services
│   ├── __init__.py
│   ├── auth.py              # Authentication & authorization
│   ├── datasets.py          # Dataset management API
│   ├── logs.py              # Logging utilities
│   └── flow_templates.py    # Template management
├── modules/              # Specialized modules
│   ├── __init__.py
│   └── deepeval_synthesizer.py # DeepEval dataset generation
├── crew/                 # CrewAI specific flows
│   ├── __init__.py
│   └── lead_score_flow.py
├── tests/                # Unit & integration tests
├── main.py               # FastAPI app entry point
└── requirements.txt      # Python dependencies
```

### Core Backend Components

#### 1. Flow Executor

```python
# core/flow_executor.py
class FlowExecutor:
    async def execute_flow(
        self,
        nodes: List[FlowNode],
        edges: List[FlowEdge],
        params: Dict[str, Any]
    ) -> FlowExecutionResult:
        # Execute flow using graph traversal
        context = {}
        executed_nodes = []

        for node in self.get_execution_order(nodes, edges):
            result = await self.execute_node(node, context)
            context.update(result.data)
            executed_nodes.append(node.id)

        return FlowExecutionResult(
            success=True,
            context=context,
            executed_nodes=executed_nodes
        )
```

#### 2. Action Registry

```python
# core/actions.py
ACTION_DEFS: Dict[str, ActionDefinition] = {}
ACTION_HANDLERS: Dict[str, Callable] = {}

def register_action(
    action_id: str,
    name: str,
    description: str,
    params: List[ActionParam],
    node_type: NodeType = NodeType.ACTION
):
    def decorator(handler: Callable):
        ACTION_DEFS[action_id] = ActionDefinition(
            id=action_id, name=name, description=description,
            params=params, node_type=node_type
        )
        ACTION_HANDLERS[action_id] = handler
        return handler
    return decorator
```

#### 3. Service Layer

```python
# services/datasets.py
router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.post("/")
async def create_dataset(
    dataset: DatasetCreate,
    current_user: User = Depends(get_current_user)
):
    # Service logic for dataset creation
    pass

@router.get("/{dataset_id}/documents")
async def get_documents(
    dataset_id: str,
    current_user: User = Depends(get_current_user)
):
    # Service logic for document retrieval
    pass
```

## 🔄 Flow Engine Architecture

### Node Types

```python
# core/models.py
class NodeType(str, Enum):
    START = "START"
    ACTION = "ACTION"
    CONDITION = "CONDITION"
    LOOP = "LOOP"
    MERGE = "MERGE"
    END = "END"
    REVIEW_GOLDENS = "REVIEW_GOLDENS"
    FILE_UPLOAD = "FILE_UPLOAD"
```

### Execution Flow

1. **Validation**: Validate flow structure and node connections
2. **Planning**: Determine execution order based on dependencies
3. **Execution**: Execute nodes in order, managing context
4. **Error Handling**: Handle failures and provide recovery options
5. **Completion**: Return results and cleanup resources

### Context Management

```python
class ExecutionContext:
    def __init__(self):
        self.data: Dict[str, Any] = {}
        self.variables: Dict[str, Any] = {}
        self.history: List[NodeExecutionResult] = []

    def set_variable(self, name: str, value: Any):
        self.variables[name] = value

    def get_variable(self, name: str, default: Any = None) -> Any:
        return self.variables.get(name, default)

    def resolve_references(self, value: str) -> Any:
        # Resolve variable references like ${nodeId.output}
        pass
```

## 🗄️ Data Layer Architecture

### Database Design

```sql
-- Core tables
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    description TEXT,
    user_id UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID REFERENCES datasets(id),
    title VARCHAR NOT NULL,
    content TEXT,
    file_path VARCHAR,
    uploaded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE goldens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    dataset_id UUID REFERENCES datasets(id),
    document_id UUID REFERENCES documents(id),
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    context TEXT[],
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Data Access Patterns

```python
# services/datasets.py
class DatasetService:
    def __init__(self, db: Database):
        self.db = db

    async def create_dataset(
        self,
        dataset: DatasetCreate,
        user_id: str
    ) -> Dataset:
        query = """
        INSERT INTO datasets (name, description, user_id)
        VALUES ($1, $2, $3)
        RETURNING *
        """
        return await self.db.fetch_one(query, dataset.name, dataset.description, user_id)

    async def get_user_datasets(self, user_id: str) -> List[Dataset]:
        query = """
        SELECT * FROM datasets
        WHERE user_id = $1
        ORDER BY created_at DESC
        """
        return await self.db.fetch_all(query, user_id)
```

## 🔌 Integration Patterns

### AI Provider Integration

```python
# services/aiService.ts
export interface AIProvider {
  name: string;
  generateResponse(prompt: string, config: AIConfig): Promise<string>;
  generateStream(prompt: string, config: AIConfig): AsyncIterable<string>;
  testConnection(config: AIConfig): Promise<boolean>;
}

export class OpenAIProvider implements AIProvider {
  name = "openai";

  async generateResponse(prompt: string, config: AIConfig): Promise<string> {
    // OpenAI API integration
  }
}
```

### External Service Integration

```python
# modules/deepeval_synthesizer.py
class DeepEvalSynthesizer:
    def __init__(self, llm_provider: str, api_key: str):
        self.llm_provider = llm_provider
        self.api_key = api_key

    async def generate_goldens(
        self,
        documents: List[str],
        config: GenerationConfig
    ) -> List[Golden]:
        # DeepEval integration for Q&A generation
        pass
```

## 🔒 Security Architecture

### Authentication Flow

```
User Login → Supabase Auth → JWT Token → Frontend Storage → API Requests
```

### Authorization Patterns

```python
# services/auth.py
async def get_current_user(
    token: str = Depends(oauth2_scheme)
) -> User:
    # Verify JWT token with Supabase
    user_info = supabase.auth.get_user(token)

    if not user_info.user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return User.from_supabase_user(user_info.user)

# Usage in routes
@router.get("/protected")
async def protected_endpoint(
    current_user: User = Depends(get_current_user)
):
    # Endpoint logic with authenticated user
    pass
```

## 📊 Performance Considerations

### Caching Strategy

```python
# Frontend: React Query for API caching
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

# Backend: Redis for frequently accessed data
import redis

class CacheService:
    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)

    async def get_cached_result(self, key: str) -> Optional[Any]:
        cached = await self.redis.get(key)
        return json.loads(cached) if cached else None
```

### Async Processing

```python
# For long-running operations like PDF processing
import asyncio
from concurrent.futures import ThreadPoolExecutor

class PDFProcessor:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def process_pdf_async(self, file_data: bytes) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._process_pdf_sync,
            file_data
        )
```

## 🔧 Development Architecture

### Module System

```python
# main.py - Dynamic module loading
ACTION_MODULES: Iterable[str] = (
    "actions.actions_crewai",
    "actions.actions_dataset",
    "actions.actions_deepeval",
)

def load_action_modules():
    for module_name in ACTION_MODULES:
        module = importlib.import_module(module_name)
        print(f"✅ Loaded {module_name}")
```

### Testing Architecture

```python
# tests/test_flow_executor.py
@pytest.mark.asyncio
async def test_flow_execution():
    executor = FlowExecutor()

    # Create test flow
    nodes = [
        FlowNode(id="start", type=NodeType.START),
        FlowNode(id="action1", type=NodeType.ACTION, data={"actionId": "test_action"})
    ]
    edges = [FlowEdge(source="start", target="action1")]

    # Execute flow
    result = await executor.execute_flow(nodes, edges, {})

    assert result.success
    assert "action1" in result.executed_nodes
```

## 🚀 Deployment Architecture

### Container Strategy

```dockerfile
# Multi-stage Dockerfile for optimization
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM python:3.9-slim AS backend
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Scaling Considerations

- **Stateless Design**: API can be horizontally scaled
- **Database Pooling**: Connection pooling for database access
- **Load Balancing**: Multiple backend instances behind load balancer
- **CDN**: Static assets served via CDN
- **Monitoring**: Health checks and metrics collection

## 📈 Future Architecture Enhancements

### Microservices Evolution

```python
# Potential future architecture
services = {
    'api-gateway': 'API routing and authentication',
    'flow-engine': 'Flow execution and orchestration',
    'ai-service': 'AI provider integrations',
    'pdf-service': 'Document processing',
    'dataset-service': 'Data management',
    'notification-service': 'Alerts and notifications'
}
```

### Event-Driven Architecture

```python
# Future: Event-driven communication
class EventBus:
    async def publish(self, event: Event):
        # Publish event to message queue
        pass

    async def subscribe(self, event_type: str, handler: Callable):
        # Subscribe to events
        pass

# Usage
await event_bus.publish(FlowStartedEvent(flow_id="123"))
```

---

This architecture provides a solid foundation for Flow Builder's current functionality while being extensible for future enhancements. The modular design ensures maintainability and the separation of concerns makes the system easier to understand and develop.

---

**Last Updated:** December 3, 2025
**Version**: 1.0.0
**Architecture**: Modular & Scalable ✅