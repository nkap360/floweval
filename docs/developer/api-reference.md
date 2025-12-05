# API Reference

Complete REST API documentation for Flow Builder backend services.

## 📋 Table of Contents

- [Authentication](#authentication)
- [Datasets API](#datasets-api)
- [Documents API](#documents-api)
- [Goldens API](#goldens-api)
- [Flow Execution API](#flow-execution-api)
- [Flow Templates API](#flow-templates-api)
- [Actions API](#actions-api)
- [Logs API](#logs-api)
- [Health & Status](#health--status)

---

## 🔐 Authentication

All API endpoints (except `/health` and `/`) require authentication via JWT tokens.

### Headers Required

```http
Authorization: Bearer <jwt_token>
X-Workspace-Id: <workspace_uuid>  # For workspace-scoped endpoints
```

### Token Structure

```json
{
  "sub": "user-uuid",
  "email": "user@example.com",
  "role": "member|admin|service_role",
  "workspace_roles": [
    {
      "workspace_id": "workspace-uuid",
      "role": "owner|admin|member"
    }
  ],
  "exp": 1735689600,
  "iat": 1735686000
}
```

### Get Auth Configuration

```http
GET /auth/model
```

**Response:**
```json
{
  "uses_supabase": true,
  "supabase_url": "https://xxx.supabase.co",
  "auth_strategy": "supabase_jwt"
}
```

---

## 📊 Datasets API

### List All Datasets

```http
GET /datasets
Authorization: Bearer <token>
```

**Response:**
```json
{
  "datasets": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Customer Support QA",
      "description": "Q&A pairs for customer support training",
      "use_case": "chatbot",
      "created_at": "2025-12-01T10:00:00Z",
      "updated_at": "2025-12-03T15:30:00Z",
      "document_count": 15,
      "golden_count": 142,
      "status": "active"
    }
  ]
}
```

### Get Dataset by ID

```http
GET /datasets/{dataset_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Customer Support QA",
  "description": "Q&A pairs for customer support training",
  "use_case": "chatbot",
  "created_at": "2025-12-01T10:00:00Z",
  "updated_at": "2025-12-03T15:30:00Z",
  "metadata": {
    "tags": ["support", "chatbot", "training"],
    "version": "1.0",
    "language": "en"
  }
}
```

### Create Dataset

```http
POST /datasets
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "New Dataset",
  "description": "Description of the dataset",
  "use_case": "rag|qa|chatbot|agent"
}
```

**Response:**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440000",
  "name": "New Dataset",
  "description": "Description of the dataset",
  "use_case": "rag",
  "created_at": "2025-12-03T16:00:00Z",
  "status": "draft"
}
```

### Update Dataset

```http
PATCH /datasets/{dataset_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Dataset Name",
  "description": "Updated description"
}
```

### Delete Dataset

```http
DELETE /datasets/{dataset_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "message": "Dataset deleted successfully",
  "id": "550e8400-e29b-41d4-a716-446655440000"
}
```

---

## 📄 Documents API

### List Documents in Dataset

```http
GET /datasets/{dataset_id}/documents
Authorization: Bearer <token>
```

**Response:**
```json
{
  "documents": [
    {
      "id": "770e8400-e29b-41d4-a716-446655440000",
      "dataset_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Installation Guide",
      "content": "# Installation\n\n...",
      "file_type": "pdf",
      "file_size": 524288,
      "page_count": 15,
      "uploaded_at": "2025-12-02T09:30:00Z",
      "metadata": {
        "source": "documentation",
        "version": "1.2"
      }
    }
  ]
}
```

### Get Document by ID

```http
GET /datasets/{dataset_id}/documents/{document_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "770e8400-e29b-41d4-a716-446655440000",
  "dataset_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Installation Guide",
  "content": "# Installation\n\nStep 1: Download...",
  "file_type": "pdf",
  "file_size": 524288,
  "page_count": 15,
  "uploaded_at": "2025-12-02T09:30:00Z"
}
```

### Upload Document

```http
POST /datasets/{dataset_id}/documents
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: <binary_file>
title: "Document Title"
```

**Response:**
```json
{
  "id": "880e8400-e29b-41d4-a716-446655440000",
  "dataset_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Document Title",
  "file_type": "pdf",
  "file_size": 1048576,
  "content": "Extracted text content...",
  "uploaded_at": "2025-12-03T16:15:00Z"
}
```

### Delete Document

```http
DELETE /datasets/{dataset_id}/documents/{document_id}
Authorization: Bearer <token>
```

---

## ⭐ Goldens API

### List Goldens in Dataset

```http
GET /datasets/{dataset_id}/goldens
Authorization: Bearer <token>
```

**Query Parameters:**
- `document_id` (optional): Filter by document
- `status` (optional): Filter by status (approved, pending, rejected)
- `limit` (optional): Number of results (default: 100)
- `offset` (optional): Pagination offset (default: 0)

**Response:**
```json
{
  "goldens": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440000",
      "dataset_id": "550e8400-e29b-41d4-a716-446655440000",
      "document_id": "770e8400-e29b-41d4-a716-446655440000",
      "question": "How do I install the application?",
      "answer": "Follow these steps: 1. Download the installer...",
      "context": "Installation section from page 3",
      "status": "approved",
      "created_at": "2025-12-02T11:00:00Z",
      "reviewed_at": "2025-12-02T14:30:00Z",
      "reviewed_by": "user-uuid",
      "metadata": {
        "source": "ai_generated",
        "confidence": 0.95
      }
    }
  ],
  "total": 142,
  "limit": 100,
  "offset": 0
}
```

### Get Golden by ID

```http
GET /datasets/{dataset_id}/goldens/{golden_id}
Authorization: Bearer <token>
```

### Create Golden

```http
POST /datasets/{dataset_id}/goldens
Authorization: Bearer <token>
Content-Type: application/json

{
  "document_id": "770e8400-e29b-41d4-a716-446655440000",
  "question": "What are the system requirements?",
  "answer": "Minimum requirements: 4GB RAM, 2GHz CPU, 500MB disk space",
  "context": "System requirements section from documentation"
}
```

**Response:**
```json
{
  "id": "aa0e8400-e29b-41d4-a716-446655440000",
  "dataset_id": "550e8400-e29b-41d4-a716-446655440000",
  "document_id": "770e8400-e29b-41d4-a716-446655440000",
  "question": "What are the system requirements?",
  "answer": "Minimum requirements: 4GB RAM, 2GHz CPU, 500MB disk space",
  "context": "System requirements section from documentation",
  "status": "pending",
  "created_at": "2025-12-03T16:20:00Z"
}
```

### Update Golden

```http
PATCH /datasets/{dataset_id}/goldens/{golden_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "question": "Updated question?",
  "answer": "Updated answer",
  "status": "approved"
}
```

### Delete Golden

```http
DELETE /datasets/{dataset_id}/goldens/{golden_id}
Authorization: Bearer <token>
```

### Bulk Operations

```http
POST /datasets/{dataset_id}/goldens/bulk
Authorization: Bearer <token>
Content-Type: application/json

{
  "operation": "approve|reject|delete",
  "golden_ids": [
    "990e8400-e29b-41d4-a716-446655440000",
    "aa0e8400-e29b-41d4-a716-446655440000"
  ]
}
```

---

## 🔄 Flow Execution API

### Execute Flow

```http
POST /flow/execute
Authorization: Bearer <token>
X-Workspace-Id: <workspace_uuid>
Content-Type: application/json

{
  "flow": {
    "nodes": [
      {
        "id": "start-1",
        "type": "start",
        "data": {
          "label": "Start"
        }
      },
      {
        "id": "action-1",
        "type": "action",
        "data": {
          "actionId": "load_dataset",
          "label": "Load Dataset",
          "params": {
            "dataset_id": "550e8400-e29b-41d4-a716-446655440000"
          }
        }
      }
    ],
    "edges": [
      {
        "id": "e1",
        "source": "start-1",
        "target": "action-1"
      }
    ]
  },
  "params": {
    "dataset_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

**Response:**
```json
{
  "execution_id": "bb0e8400-e29b-41d4-a716-446655440000",
  "status": "running|completed|failed",
  "started_at": "2025-12-03T16:25:00Z",
  "completed_at": "2025-12-03T16:26:30Z",
  "results": {
    "action-1": {
      "status": "success",
      "output": {
        "dataset": {...},
        "document_count": 15,
        "golden_count": 142
      }
    }
  },
  "logs": [
    {
      "timestamp": "2025-12-03T16:25:00Z",
      "level": "info",
      "node_id": "start-1",
      "message": "Flow execution started"
    },
    {
      "timestamp": "2025-12-03T16:25:05Z",
      "level": "info",
      "node_id": "action-1",
      "message": "Loading dataset..."
    }
  ]
}
```

### Get Execution Status

```http
GET /flow/executions/{execution_id}
Authorization: Bearer <token>
```

### Get Execution Logs

```http
GET /flow/executions/{execution_id}/logs
Authorization: Bearer <token>
```

**Query Parameters:**
- `level` (optional): Filter by log level (debug, info, warning, error)
- `node_id` (optional): Filter by node ID

**Response:**
```json
{
  "execution_id": "bb0e8400-e29b-41d4-a716-446655440000",
  "logs": [
    {
      "timestamp": "2025-12-03T16:25:00Z",
      "level": "info",
      "node_id": "start-1",
      "message": "Flow execution started"
    }
  ]
}
```

---

## 📋 Flow Templates API

### List All Templates

```http
GET /flow/templates
Authorization: Bearer <token>
```

**Response:**
```json
{
  "templates": [
    {
      "id": "template-pdf-to-golden",
      "name": "PDF to Golden Dataset",
      "description": "Extract Q&A pairs from PDF documents",
      "category": "data_generation",
      "icon": "file-text",
      "nodes": [...],
      "edges": [...],
      "required_params": [
        {
          "name": "dataset_id",
          "label": "Dataset ID",
          "type": "string",
          "required": true
        }
      ]
    }
  ]
}
```

### Get Template by ID

```http
GET /flow/templates/{template_id}
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "template-pdf-to-golden",
  "name": "PDF to Golden Dataset",
  "description": "Extract Q&A pairs from PDF documents",
  "category": "data_generation",
  "version": "1.0.0",
  "nodes": [
    {
      "id": "start",
      "type": "start",
      "position": {"x": 100, "y": 100},
      "data": {"label": "Start"}
    },
    {
      "id": "upload",
      "type": "file_upload",
      "position": {"x": 300, "y": 100},
      "data": {
        "label": "Upload PDF",
        "acceptedFileTypes": [".pdf"]
      }
    }
  ],
  "edges": [
    {
      "id": "e1",
      "source": "start",
      "target": "upload"
    }
  ],
  "required_params": [...]
}
```

---

## ⚙️ Actions API

### List Actions for Node Type

```http
GET /node-types/{node_type}/actions
Authorization: Bearer <token>
```

**Node Types:**
- `action` - Backend action nodes
- `review` - Review nodes
- `export` - Export nodes

**Response:**
```json
{
  "actions": [
    {
      "id": "load_dataset",
      "name": "Load Dataset",
      "description": "Load an existing dataset with documents and goldens",
      "node_type": "action",
      "params": [
        {
          "name": "dataset_id",
          "label": "Dataset ID",
          "type": "string",
          "required": true,
          "description": "UUID of the dataset to load"
        }
      ],
      "outputs": [
        {
          "name": "dataset",
          "type": "object",
          "description": "Loaded dataset object"
        }
      ]
    }
  ]
}
```

### Get Action Details

```http
GET /actions/{action_id}
Authorization: Bearer <token>
```

---

## 📝 Logs API

### Query Logs

```http
GET /logs
Authorization: Bearer <token>
```

**Query Parameters:**
- `level` (optional): Filter by level (debug, info, warning, error)
- `start_time` (optional): ISO 8601 timestamp
- `end_time` (optional): ISO 8601 timestamp
- `execution_id` (optional): Filter by execution
- `limit` (optional): Max results (default: 100)

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2025-12-03T16:30:00Z",
      "level": "info",
      "service": "flow_executor",
      "execution_id": "bb0e8400-e29b-41d4-a716-446655440000",
      "message": "Node executed successfully",
      "metadata": {
        "node_id": "action-1",
        "duration_ms": 1250
      }
    }
  ],
  "total": 1547,
  "limit": 100
}
```

---

## 🏥 Health & Status

### Health Check

```http
GET /health
```

No authentication required.

**Response:**
```json
{
  "status": "healthy",
  "service": "flowbuilder-backend",
  "version": "1.0.0",
  "timestamp": "2025-12-03T16:35:00Z",
  "dependencies": {
    "database": "connected",
    "supabase": "connected",
    "ai_providers": "configured"
  }
}
```

### Root Endpoint

```http
GET /
```

**Response:**
```json
{
  "name": "Flow Builder API",
  "version": "1.0.0",
  "status": "running",
  "docs": "/docs",
  "health": "/health",
  "timestamp": "2025-12-03T16:35:00Z"
}
```

---

## 🔧 Error Responses

All endpoints return consistent error responses:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "Additional context"
    }
  }
}
```

### Common HTTP Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request format or parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource conflict (duplicate, etc.) |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Error Codes

```
AUTH_INVALID_TOKEN - JWT token invalid or expired
AUTH_MISSING_TOKEN - Authorization header missing
AUTH_INSUFFICIENT_PERMISSIONS - User lacks required permissions
RESOURCE_NOT_FOUND - Requested resource doesn't exist
VALIDATION_ERROR - Request validation failed
RATE_LIMIT_EXCEEDED - Too many requests
INTERNAL_ERROR - Unexpected server error
```

---

## 📊 Rate Limits

Default rate limits per API key:

- **Standard**: 100 requests/minute
- **Burst**: 10 requests/second
- **Daily**: 10,000 requests/day

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1735689660
```

---

## 🔐 Best Practices

### Authentication

1. **Store tokens securely** in environment variables or secure storage
2. **Rotate tokens regularly** (recommended: every 30 days)
3. **Use workspace-scoped tokens** for multi-tenant applications
4. **Implement token refresh** before expiration

### API Calls

1. **Use pagination** for large result sets
2. **Implement retry logic** with exponential backoff
3. **Cache responses** when appropriate
4. **Handle rate limits** gracefully
5. **Validate data** before sending requests

### Error Handling

```typescript
try {
  const response = await fetch('/api/datasets', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message);
  }

  return await response.json();
} catch (error) {
  console.error('API call failed:', error);
  // Handle error appropriately
}
```

---

## 📚 Additional Resources

- [Authentication Guide](../deployment/security.md)
- [Architecture Overview](architecture.md)
- [Backend README](../../backend/README.md)
- [Developer Guide](DEVELOPER.md)

---

**API Version:** 1.0.0  
**Last Updated:** December 3, 2025  
**Status:** Production Ready ✅
