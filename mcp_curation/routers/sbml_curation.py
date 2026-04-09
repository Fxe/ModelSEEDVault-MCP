from typing import Literal

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, Path, Query

from mcp_curation.client import sbml_client

_MODEL_TYPE_SBML: Literal["sbml"] = "sbml"
_MODEL_TYPE_COBRA: Literal["cobra"] = "cobra"

_MODEL_TYPE_MAP = {
    _MODEL_TYPE_SBML: sbml_client.NODE_TYPE_SBML_MODEL,
    _MODEL_TYPE_COBRA: sbml_client.NODE_TYPE_COBRA_MODEL,
}

_MODEL_TYPE_QUERY = Query(default=_MODEL_TYPE_SBML, description="Model node type: 'sbml' for SBMLModel, 'cobra' for COBRAModel")

router = APIRouter(prefix="/sbml-curation", tags=["sbml-curation"])

_MODEL_ID = Path(example="iAbaylyiv4")
_COMPARTMENT_ID = Path(example="c")
_SPECIES_ID = Path(example="M_atp_c")
_REACTION_ID = Path(example="R_PGI")
_REACTION_EID = Path(example="4:3779b88f-90cb-49d4-a69d-a7360263bf82:2364")
_GENE_ID = Path(example="b4025")


class AnnotationCreateRequest(BaseModel):
    subject_eid: str
    object: str
    agent_id: str
    method: str
    comment: str


def _model_scoped_entity_eid(model_id: str, entity_id: str) -> str:
    return f"{model_id}:{entity_id}"


@router.get("/config")
def sbml_curation_config() -> dict[str, object]:
    return sbml_client.config()


def _handle_sbml_error(exc: sbml_client.SBMLApiError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/models")
def list_models(model_type: Literal["sbml", "cobra"] = _MODEL_TYPE_QUERY) -> object:
    try:
        return sbml_client.list_models(_MODEL_TYPE_MAP[model_type])
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}")
def get_model(model_id: str = _MODEL_ID, model_type: Literal["sbml", "cobra"] = _MODEL_TYPE_QUERY) -> object:
    try:
        return sbml_client.get_model(model_id)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/compartments")
def list_model_compartments(model_id: str = _MODEL_ID, model_type: Literal["sbml", "cobra"] = _MODEL_TYPE_QUERY) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_COMPARTMENT, _MODEL_TYPE_MAP[model_type])
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/species")
def list_model_species(model_id: str = _MODEL_ID, model_type: Literal["sbml", "cobra"] = _MODEL_TYPE_QUERY) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_SPECIES, _MODEL_TYPE_MAP[model_type])
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/reactions")
def list_model_reactions(model_id: str = _MODEL_ID, model_type: Literal["sbml", "cobra"] = _MODEL_TYPE_QUERY) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_REACTION, _MODEL_TYPE_MAP[model_type])
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/genes")
def list_model_genes(model_id: str = _MODEL_ID, model_type: Literal["sbml", "cobra"] = _MODEL_TYPE_QUERY) -> object:
    try:
        return sbml_client.list_model_children(model_id, sbml_client.EDGE_HAS_GENE, _MODEL_TYPE_MAP[model_type])
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.post("/annotation")
def add_annotation_event(payload: AnnotationCreateRequest) -> object:
    try:
        return sbml_client.add_curation_event(
            payload.subject_eid,
            payload.object,
            payload.agent_id,
            payload.method,
            payload.comment
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/compartment/{compartment_id}/annotation")
def list_compartment_annotation(
    model_id: str = _MODEL_ID,
    compartment_id: str = _COMPARTMENT_ID,
) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLCompartment',
            _model_scoped_entity_eid(model_id, compartment_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/species/{species_id}/annotation")
def list_species_annotation(
    model_id: str = _MODEL_ID,
    species_id: str = _SPECIES_ID,
) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLSpecies',
            _model_scoped_entity_eid(model_id, species_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.post("/models/{model_id}/reaction/{reaction_id}/inference")
def infer_reaction_annotation(
    model_id: str = _MODEL_ID,
    reaction_id: str = _REACTION_EID,
) -> object:
    try:
        return sbml_client.infer_model_reaction_annotation(model_id, reaction_id)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.post("/models/{model_id}/reaction/inference")
def infer_reaction_annotation(
    model_id: str = _MODEL_ID,
) -> object:
    try:
        return sbml_client.infer_model_all_reaction_annotation(model_id)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/reaction/{reaction_id}/annotation")
def list_reaction_annotation(
    model_id: str = _MODEL_ID,
    reaction_id: str = _REACTION_ID,
) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLReaction',
            _model_scoped_entity_eid(model_id, reaction_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/models/{model_id}/gene/{gene_id}/annotation")
def list_gene_annotation(
    model_id: str = _MODEL_ID,
    gene_id: str = _GENE_ID,
) -> object:
    try:
        return sbml_client.list_curation_events(
            'SBMLGene',
            _model_scoped_entity_eid(model_id, gene_id)
        )
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)
