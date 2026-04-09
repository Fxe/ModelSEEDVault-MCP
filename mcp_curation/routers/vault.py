from fastapi import APIRouter, HTTPException, Path

from mcp_curation.client import sbml_client

router = APIRouter(prefix="/vault", tags=["vault"])

_NODE_UID = Path(example="4:3779b88f-90cb-49d4-a69d-a7360263bf82:2364")


def _handle_sbml_error(exc: sbml_client.SBMLApiError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/node/from-uid/{uid}")
def get_node_from_uid(uid: str = _NODE_UID) -> object:
    try:
        return sbml_client.get_node_by_element_id(uid)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)
