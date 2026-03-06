# MCP Server for modelseed-vault

Initial Python/FastAPI MCP server scaffold for ModelSEEDVault SBML curation.

## Install

```bash
pip install -e .
```

## Run combined server (FastAPI + FastMCP)

```bash
uvicorn mcp_curation.main:app --reload
```

### Configure SBML backend endpoint

Default backend URL:

- `http://192.168.1.202:8080`

Override it with:

```bash
export SBML_API_BASE_URL="http://192.168.1.202:8080"
uvicorn mcp_curation.main:app --reload
```

FastMCP is mounted into FastAPI at:

- `/mcp`

## First routes

- `GET /health`
- `GET /sbml-curation/config`
- `GET /sbml-curation/models`
- `GET /sbml-curation/models/{model_id}/compartments`
- `GET /sbml-curation/models/{model_id}/species`
- `GET /sbml-curation/models/{model_id}/reactions`
- `GET /sbml-curation/models/{model_id}/genes`

## Docs

- Swagger UI: `http://127.0.0.1:8000/docs`

## FastMCP tools

- `sbml_curation_config`
- `list_models`
- `list_model_compartments`
- `list_model_species`
- `list_model_reactions`
- `list_model_genes`
