from fastmcp import FastMCP

from mcp_curation.client import sbml_client

mcp = FastMCP(name="ModelSEEDVault SBML Curation")


def _run_with_sbml_errors(fn, *args):
    try:
        return fn(*args)
    except sbml_client.SBMLApiError as exc:
        raise RuntimeError(exc.detail) from exc


def build_mcp_asgi_app():
    """Create an ASGI app from FastMCP across supported FastMCP versions."""
    factory_names = (
        "http_app",
        "streamable_http_app",
        "sse_app",
        "asgi_app",
    )
    for name in factory_names:
        factory = getattr(mcp, name, None)
        if callable(factory):
            try:
                return factory()
            except TypeError:
                continue

    app_attr = getattr(mcp, "app", None)
    if app_attr is not None:
        return app_attr

    tried = ", ".join(factory_names + ("app",))
    raise RuntimeError(f"Could not build FastMCP ASGI app. Tried: {tried}")


@mcp.tool()
def sbml_curation_config() -> dict[str, object]:
    """Return active SBML backend configuration."""
    return sbml_client.config()


@mcp.tool()
def list_models() -> object:
    """List SBML models from backend graph service."""
    return _run_with_sbml_errors(sbml_client.list_models)


@mcp.tool()
def list_model_compartments(model_id: str) -> object:
    """List model compartments via has_sbml_compartment."""
    return _run_with_sbml_errors(
        sbml_client.list_model_children,
        model_id,
        sbml_client.EDGE_HAS_COMPARTMENT,
    )


@mcp.tool()
def list_model_species(model_id: str) -> object:
    """List model species via has_sbml_species."""
    return _run_with_sbml_errors(
        sbml_client.list_model_children,
        model_id,
        sbml_client.EDGE_HAS_SPECIES,
    )


@mcp.tool()
def list_model_reactions(model_id: str) -> object:
    """List model reactions via has_sbml_reaction."""
    return _run_with_sbml_errors(
        sbml_client.list_model_children,
        model_id,
        sbml_client.EDGE_HAS_REACTION,
    )


@mcp.tool()
def list_model_genes(model_id: str) -> object:
    """List model genes via has_sbml_gene."""
    return _run_with_sbml_errors(
        sbml_client.list_model_children,
        model_id,
        sbml_client.EDGE_HAS_GENE,
    )


if __name__ == "__main__":
    mcp.run()
