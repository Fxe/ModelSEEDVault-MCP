import os
import secrets
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials, HTTPBearer

from mcp_curation.mcp_server import build_mcp_asgi_app
from mcp_curation.routers.genome_annotation import router as genome_annotation_router
from mcp_curation.routers.sbml_curation import router as sbml_curation_router
from mcp_curation.routers.vault import router as vault_router

_MCP_MOUNT_PATH = "/mcp"
_MCP_API_KEY_ENV = "MCP_API_KEY"
_CORS_ALLOW_ORIGINS_ENV = "CORS_ALLOW_ORIGINS"
_AUTO_KEY_NBYTES = 24
_PUBLIC_PATHS = {"/health", "/openapi.json", "/docs", "/redoc"}
_PUBLIC_PREFIXES = {"/vault/"}
_effective_mcp_api_key = ""
_mcp_api_key_source = "uninitialized"
_bearer_scheme = HTTPBearer(auto_error=False)
_api_key_header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)


def _mcp_api_key() -> str:
    return _effective_mcp_api_key


def _cors_allow_origins() -> list[str]:
    configured_origins = os.getenv(_CORS_ALLOW_ORIGINS_ENV, "").strip()
    if configured_origins:
        return [origin.strip() for origin in configured_origins.split(",") if origin.strip()]
    return ["http://192.168.1.164:62699"]


def _extract_api_key(request: Request) -> str:
    auth_header = request.headers.get("authorization", "")
    if auth_header.lower().startswith("bearer "):
        return auth_header[7:].strip()
    return request.headers.get("x-api-key", "").strip()


def _initialize_mcp_api_key() -> None:
    global _effective_mcp_api_key
    global _mcp_api_key_source

    configured_api_key = os.getenv(_MCP_API_KEY_ENV, "").strip()
    if configured_api_key:
        _effective_mcp_api_key = configured_api_key
        _mcp_api_key_source = "env"
        return

    _effective_mcp_api_key = secrets.token_urlsafe(_AUTO_KEY_NBYTES)
    _mcp_api_key_source = "generated"
    print(
        f"[mcp] {_MCP_API_KEY_ENV} not set. Generated API key for this process:\n"
        f"{_effective_mcp_api_key}"
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    _initialize_mcp_api_key()
    yield


app = FastAPI(
    title="ModelSEEDVault MCP Server",
    version="0.1.0",
    description="Initial MCP server routes for SBML curation",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_allow_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)


def require_api_key_openapi(
    bearer_credentials: HTTPAuthorizationCredentials | None = Security(_bearer_scheme),
    header_api_key: str | None = Security(_api_key_header_scheme),
) -> None:
    expected_api_key = _mcp_api_key()
    if not expected_api_key:
        raise HTTPException(status_code=500, detail=f"{_MCP_API_KEY_ENV} is not configured")

    provided_api_key = header_api_key or (bearer_credentials.credentials if bearer_credentials else "")
    if provided_api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")


app.include_router(sbml_curation_router, dependencies=[Depends(require_api_key_openapi)])
app.include_router(genome_annotation_router, dependencies=[Depends(require_api_key_openapi)])
app.include_router(vault_router)


@app.middleware("http")
async def require_mcp_api_key(request: Request, call_next):
    path = request.url.path
    is_public_path = path in _PUBLIC_PATHS or any(path.startswith(p) for p in _PUBLIC_PREFIXES)
    if request.method == "OPTIONS" or is_public_path:
        return await call_next(request)

    expected_api_key = _mcp_api_key()
    if not expected_api_key:
        return JSONResponse(
            status_code=500,
            content={"detail": f"{_MCP_API_KEY_ENV} is not configured"},
        )

    provided_api_key = _extract_api_key(request)
    if provided_api_key != expected_api_key:
        return JSONResponse(
            status_code=401,
            content={"detail": "Invalid API key"},
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await call_next(request)


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
            "api_key_required": True,
            "api_key_env_var": _MCP_API_KEY_ENV,
            "api_key_source": _mcp_api_key_source,
            "cors_allow_origins_env_var": _CORS_ALLOW_ORIGINS_ENV,
            "cors_allow_origins": _cors_allow_origins(),
            "public_paths": sorted(_PUBLIC_PATHS),
        },
    }
