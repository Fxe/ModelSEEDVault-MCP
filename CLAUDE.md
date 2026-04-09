# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

MCP server for ModelSEEDVault SBML curation. Combines a FastAPI REST API with a FastMCP (Model Context Protocol) server, both backed by an external SBML graph service.

## Development setup

Use Python 3.11 and `uv`:

```bash
uv venv --python 3.11 .venv
source .venv/bin/activate
uv pip install -e .
```

## Running the server

```bash
MCP_API_KEY='change-me' \
SBML_API_BASE_URL='http://localhost:8080' \
uv run --python .venv/bin/python uvicorn mcp_curation.main:app --host 127.0.0.1 --port 8000 --reload
```

Environment variables:
- `MCP_API_KEY` — API key for auth (auto-generated at startup if unset)
- `SBML_API_BASE_URL` — SBML backend URL (default: `http://localhost:8080`)
- `CORS_ALLOW_ORIGINS` — comma-separated allowed origins (default: `http://192.168.1.164:62699`)

## Architecture

```
HTTP Request
    → CORS middleware
    → API key auth middleware (Bearer or X-API-Key; skips /health, /docs, /redoc, /openapi.json)
    ├─→ FastAPI router (/sbml-curation/*)       → sbml_client.py → SBML backend
    ├─→ FastAPI router (/genome-annotation/*)   → sbml_client.py → SBML backend
    └─→ FastMCP ASGI app (/mcp/*)               → MCP tools → sbml_client.py → SBML backend
```

**`mcp_curation/main.py`** — FastAPI app entry point. Configures CORS, auth middleware, mounts FastMCP at `/mcp`, includes the sbml-curation and genome-annotation routers.

**`mcp_curation/mcp_server.py`** — FastMCP server. Registers 6 MCP tools (`sbml_curation_config`, `list_models`, `list_model_compartments`, `list_model_species`, `list_model_reactions`, `list_model_genes`) that delegate to `sbml_client.py`.

**`mcp_curation/routers/sbml_curation.py`** — FastAPI route handlers under `/sbml-curation/`. Endpoints: list/get models, list compartments/species/reactions/genes per model, add and list annotation events, infer reaction annotations.

**`mcp_curation/routers/genome_annotation.py`** — FastAPI route handlers under `/genome-annotation/`. Endpoints:
- `GET /genome` — list all `Genome` nodes
- `GET /genome/{genome_id}/contigs` — `Genome -has_contig-> GenomicContig`
- `GET /genome/{genome_id}/features` — 2-step traversal: `Genome -has_contig-> GenomicContig -has_feature-> GenomicFeature`

**`mcp_curation/client/sbml_client.py`** — HTTP client (stdlib `urllib`, no external HTTP library) for the SBML backend graph service. Key functions: `list_node_children(node_type, node_key, edge_type)`, `add_curation_event`, `list_curation_events`. Raises `SBMLApiError` on failures.

### Graph traversal response format

`/graph/node/{type}/{id}/child` returns `List[[EDGE, NODE]]` — each row is a two-element list where index 0 is the relationship and index 1 is the child `Neo4jNodeEntity`. The node's `entry` field is the key used for further graph lookups.

## Contributor expectations (from AGENTS.md)

- Work only inside `mcp_curation/` unless explicitly asked otherwise.
- Update `README.md` when behavior or setup changes.
- Do not add dependencies unless necessary.
- If `setup.py` is changed, verify install/build still works.
- Summarize changed files and validation steps after edits.
