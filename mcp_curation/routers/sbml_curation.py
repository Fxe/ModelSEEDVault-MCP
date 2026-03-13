from pydantic import BaseModel
from fastapi import APIRouter, HTTPException

from mcp_curation.client import sbml_client

router = APIRouter(prefix="/sbml-curation", tags=["sbml-curation"])


class AnnotationCreateRequest(BaseModel):
    subject_eid: str
    object: str
    agent_id: str


def _model_scoped_entity_eid(model_id: str, entity_id: str) -> str:
    return f"{model_id}:{entity_id}"


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


@router.post("/annotation")
def add_annotation_event(payload: AnnotationCreateRequest) -> object:
    try:
        return sbml_client.add_curation_event(
            payload.subject_eid,
            payload.object,
            payload.agent_id,
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/compartment/{compartment_id}/annotation")
def list_compartment_annotation(model_id: str, compartment_id: str) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLCompartment',
            _model_scoped_entity_eid(model_id, compartment_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/species/{species_id}/annotation")
def list_species_annotation(model_id: str, species_id: str) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLSpecies',
            _model_scoped_entity_eid(model_id, species_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/reaction/{reaction_id}/annotation")
def list_reaction_annotation(model_id: str, reaction_id: str) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLReaction',
            _model_scoped_entity_eid(model_id, reaction_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/gene/{gene_id}/annotation")
def list_gene_annotation(model_id: str, gene_id: str) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLGene',
            _model_scoped_entity_eid(model_id, gene_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)
