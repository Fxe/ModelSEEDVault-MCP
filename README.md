# MCP Server for modelseed-vault

Initial Python/FastAPI MCP server scaffold for ModelSEEDVault SBML curation.

## Run

```bash
pip install fastapi "uvicorn[standard]"
uvicorn mcp_curation.main:app --reload
```

## First routes

- `GET /health`
- `GET /sbml-curation/models`
- `GET /sbml-curation/models/{model_id}/compartments`
- `GET /sbml-curation/models/{model_id}/species`
- `GET /sbml-curation/models/{model_id}/reactions`
- `GET /sbml-curation/models/{model_id}/genes`

## Docs

- Swagger UI: `http://127.0.0.1:8000/docs`
