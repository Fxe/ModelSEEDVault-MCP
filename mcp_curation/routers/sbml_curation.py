from fastapi import APIRouter, HTTPException

from mcp_curation.client import sbml_client

router = APIRouter(prefix="/sbml-curation", tags=["sbml-curation"])

@router.get("/config")
def sbml_curation_config() -> dict[str, object]:
    return sbml_client.config()


def _handle_sbml_error(exc: sbml_client.SBMLApiError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/models")
def list_models() -> object:
    try:
        return sbml_client.list_models()
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/compartments")
def list_model_compartments(model_id: str) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_COMPARTMENT)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/species")
def list_model_species(model_id: str) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_SPECIES)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/reactions")
def list_model_reactions(model_id: str) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_REACTION)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/genes")
def list_model_genes(model_id: str) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_GENE)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)
