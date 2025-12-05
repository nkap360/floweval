# Flow Builder Backend

This FastAPI application powers the Flow Builder front end with endpoints for listing available node actions, uploading evaluation datasets, and executing directed graphs of nodes. Action modules register themselves at import time so new functionality can be added without changing the router wiring.

## Features
- **Action catalog** – exposes available node actions grouped by node type for the Flow Builder UI.
- **Dataset ingestion** – accepts CSV, PDF, Markdown, and text uploads, persisting them under `data/` and creating a lightweight golden set representation.
- **Flow execution** – performs a topological traversal of nodes, invoking registered action handlers in order and returning per-node results.

## Project layout
- `main.py` – application factory, CORS configuration, and route inclusion.
- `actions_*.py` – action definitions and handlers registered for the Flow Builder (datasets, deepeval, CrewAI, etc.).
- `flow_executor.py` – execution engine and `/flows/execute` endpoint.
- `datasets.py` – dataset upload API and in-memory registry.
- `models.py` – Pydantic schemas shared across the backend and front end.

## Getting started
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Run the API locally:
   ```bash
   uvicorn backend.main:app --reload
   ```
   The backend honors `BACKEND_LOG_LEVEL` from your environment (see `.env` for defaults) to control console and file logging verbosity.
3. Visit `http://localhost:8000/docs` for the interactive OpenAPI documentation.

## API overview
- `GET /node-types/{node_type}/actions` – list action definitions for a given `NodeType` value.
- `POST /datasets/upload` – upload a dataset file (CSV, PDF, Markdown, or plain text). Returns a `dataset_id` that can be referenced by flow nodes.
- `POST /flows/execute` – execute a flow graph described by nodes and edges. The executor runs actions in topological order, skips nodes without actions, and reports errors for cycles or unknown actions.

## Authentication & workspace authorization
- All endpoints require a `Bearer` token signed with `SUPABASE_JWT_SECRET` and, for workspace-scoped routes, an `X-Workspace-Id` header. Tokens can embed `workspace_roles` claims or rely on Supabase lookups when `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are configured.
- In production, set `SUPABASE_JWT_SECRET` to your Supabase JWT signing secret; the backend falls back to a noisy, insecure default for development only.
- Use the included helper to introspect configuration: `GET /auth/model`.
- Example dev token (valid for 1 hour):
  ```bash
  python - <<'PY'
  from datetime import datetime, timedelta
  from jose import jwt

  secret = "dev-insecure-secret"  # override with SUPABASE_JWT_SECRET
  payload = {
      "sub": "developer",
      "email": "dev@example.com",
      "exp": datetime.utcnow() + timedelta(hours=1),
      "workspace_roles": [
          {"workspace_id": "ws-ground-truth", "group_id": "grp-ops", "role": "workspace_admin"}
      ],
  }
  print(jwt.encode(payload, secret, algorithm="HS256"))
  PY
  ```

### Supabase workspace schema
- Run `backend/supabase_migrations.sql` in Supabase to provision `workspaces`, `workspace_groups`, and `workspace_memberships` with row-level security and service-role policies that the backend uses for membership validation. The script backfills access levels (`collaborative` vs `read_only`), enforces constraints, and seeds four example spaces (a default read-only workspace, Ground Truth, Analytics Sandbox, and Automation Lab) with groups and viewer/member/admin memberships so you can verify access checks immediately.
- When `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are set, the backend validates workspace membership against Supabase and merges those records with any `workspace_roles` claims in the token.
- To apply the SQL against your Supabase project, export a `SUPABASE_DB_URL` Postgres connection string (from Supabase dashboard > Settings > Database) and run:
  ```bash
  ./scripts/apply_supabase_migrations.sh
  ```
  The helper will use the Supabase CLI if installed, otherwise it falls back to `psql`.

## Testing
Automated tests validate the contracts used by the Flow Builder UI:
- The action catalog exposes dataset upload/load actions.
- Dataset uploads are persisted and consumable inside a flow execution.
- Cyclic graphs are rejected.
- Unknown actions surface clear error responses.

Run the suite with:
```bash
pytest backend/tests
```

## Production readiness notes
- Swap the in-memory dataset registry for persistent storage (e.g., Postgres or S3) to survive restarts.
- Gate CORS origins to trusted hosts.
- Add authentication around dataset upload and flow execution endpoints as needed.
- Expand action handlers to cover the full set of production node types used by the Flow Builder.
