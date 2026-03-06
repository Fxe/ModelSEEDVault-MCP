from fastapi import FastAPI

from mcp_curation.mcp_server import build_mcp_asgi_app
from mcp_curation.routers.sbml_curation import router as sbml_curation_router

app = FastAPI(
    title="ModelSEEDVault MCP Server",
    version="0.1.0",
    description="Initial MCP server routes for SBML curation",
)

app.include_router(sbml_curation_router)

_MCP_MOUNT_PATH = "/mcp"
_mcp_mount_status = "mounted"
try:
    app.mount(_MCP_MOUNT_PATH, build_mcp_asgi_app())
except Exception as exc:
    _mcp_mount_status = f"mount_failed: {exc}"


@app.get("/health")
def health() -> dict[str, object]:
    return {
        "status": "ok",
        "mcp": {
            "mount_path": _MCP_MOUNT_PATH,
            "mount_status": _mcp_mount_status,
        },
    }
