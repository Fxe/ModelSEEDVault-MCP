from fastapi import FastAPI

from mcp_curation.routers.sbml_curation import router as sbml_curation_router

app = FastAPI(
    title="ModelSEEDVault MCP Server",
    version="0.1.0",
    description="Initial MCP server routes for SBML curation",
)

app.include_router(sbml_curation_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

