# MCP Server for modelseed-vault

Initial Python/FastAPI MCP server scaffold for ModelSEEDVault SBML curation.

## Quickstart

`.venv/` is intentionally ignored by git. Each developer should create their own local virtual environment in that directory. Use Python 3.11 for consistency:

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
```

Install the project into that environment:

```bash
uv pip install -e .
```

Run the server with your local virtualenv Python:

```bash
SBML_API_BASE_URL='http://192.168.1.202:8080/' \
uv run --python .venv/bin/python uvicorn mcp_curation.main:app --host 127.0.0.1 --port 8000 --reload
```

If auth is enabled in your environment, include the API key too:

```bash
MCP_API_KEY='change-me' \
SBML_API_BASE_URL='http://192.168.1.202:8080/' \
uv run --python .venv/bin/python uvicorn mcp_curation.main:app --host 127.0.0.1 --port 8000 --reload
```

## Install

```bash
pip install -e .
```

## Run combined server (FastAPI + FastMCP)

```bash
export MCP_API_KEY="change-me"
uvicorn mcp_curation.main:app --host 127.0.0.1 --port 8000 --reload
```

### Configure SBML backend endpoint

Default backend URL:

- `http://localhost:8080`

Override it with:

```bash
export SBML_API_BASE_URL="http://localhost:8080"
export MCP_API_KEY="change-me"
uvicorn mcp_curation.main:app --host 127.0.0.1 --port 8000 --reload
```

### Configure CORS for frontend development

Default allowed frontend origin:

- `http://192.168.1.164:62699`

Override it with a comma-separated list:

```bash
export CORS_ALLOW_ORIGINS="http://192.168.1.164:62699,http://localhost:3000"
```

The server allows:

- Methods: `GET`, `POST`, `OPTIONS`
- Headers: `Authorization`, `Content-Type`, `X-API-Key`

Unauthenticated `OPTIONS` preflight requests are allowed so browser CORS checks succeed before authenticated API calls.

FastMCP is mounted into FastAPI at:

- `/mcp`

MCP auth:

- Required env var: `MCP_API_KEY` (or auto-generated at startup if unset)
- Send either:
  - `Authorization: Bearer <MCP_API_KEY>`
  - `X-API-Key: <MCP_API_KEY>`
- Applied to all non-public routes, including `/mcp/*` and `/sbml-curation/*`.
- Public routes (no API key required):
  - `/health`
  - `/docs`
  - `/redoc`
  - `/openapi.json`

Example:

```bash
curl -H "Authorization: Bearer $MCP_API_KEY" \
  http://127.0.0.1:8000/sbml-curation/models
```

Testing in Swagger `/docs`:

- Click `Authorize`.
- You can use either:
  - `HTTPBearer`: enter just the API key value.
  - `APIKeyHeader`: enter the API key value for `X-API-Key`.
- Run any `/sbml-curation/*` endpoint from the docs UI.

## First routes

- `GET /health`
- `GET /sbml-curation/config`
- `GET /sbml-curation/models`
- `GET /sbml-curation/models/{model_id}/compartments`
- `GET /sbml-curation/models/{model_id}/species`
- `GET /sbml-curation/models/{model_id}/reactions`
- `GET /sbml-curation/models/{model_id}/genes`
- `POST /sbml-curation/annotation`
- `GET /sbml-curation/models/{model_id}/compartment/{compartment_id}/annotation`
- `GET /sbml-curation/models/{model_id}/species/{species_id}/annotation`
- `GET /sbml-curation/models/{model_id}/reaction/{reaction_id}/annotation`
- `GET /sbml-curation/models/{model_id}/gene/{gene_id}/annotation`

## Docs

- Swagger UI: `http://127.0.0.1:8000/docs`

## FastMCP tools

- `sbml_curation_config`
- `list_models`
- `list_model_compartments`
- `list_model_species`
- `list_model_reactions`
- `list_model_genes`

## SBML client helpers

- `mcp_curation.client.sbml_client.add_curation_event(subject_eid, object, agent_id)`
  posts to `/graph/edge/{src}/{dst}/has_annotation_event?agent=...`
- `mcp_curation.client.sbml_client.list_curation_events(subject_eid)`
  gets `/graph/node/{subject_eid}/child?edgeType=has_annotation_event`
