import json
import os
from urllib import error, parse, request

DEFAULT_SBML_API_BASE_URL = "http://localhost:8080"
REQUEST_TIMEOUT_SECONDS = 20
NODE_TYPE_SBML_MODEL = "SBMLModel"
NODE_TYPE_COBRA_MODEL = "COBRAModel"
EDGE_HAS_COMPARTMENT = "has_compartment"
EDGE_HAS_SPECIES = "has_species"
EDGE_HAS_REACTION = "has_reaction"
EDGE_HAS_GENE = "has_gene"
EDGE_HAS_ANNOTATION_EVENT = "has_annotation_event"


class SBMLApiError(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def api_base_url() -> str:
    return os.getenv("SBML_API_BASE_URL", DEFAULT_SBML_API_BASE_URL).rstrip("/")


def config() -> dict[str, object]:
    return {
        "sbml_api_base_url": api_base_url(),
        "request_timeout_seconds": REQUEST_TIMEOUT_SECONDS,
    }


def request_graph_json(
    path: str,
    query: dict[str, str] | None = None,
    *,
    method: str = "GET",
    data: bytes | None = None,
    json_body: dict | None = None,
) -> object:
    query_string = f"?{parse.urlencode(query)}" if query else ""
    url = f"{api_base_url()}{path}{query_string}"

    headers = {"accept": "*/*"}
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(
        url=url,
        data=data,
        method=method,
        headers=headers,
    )



    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
            if not body:
                return {}
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return body
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SBMLApiError(
            status_code=exc.code,
            detail=f"SBML API returned HTTP {exc.code}: {detail or exc.reason}",
        ) from exc
    except error.URLError as exc:
        raise SBMLApiError(
            status_code=502,
            detail=f"Failed to connect to SBML API at {api_base_url()}: {exc.reason}",
        ) from exc


def fetch_graph_json(path: str, query: dict[str, str] | None = None) -> object:
    return request_graph_json(path, query)


def list_models(node_type: str = NODE_TYPE_SBML_MODEL) -> object:
    return fetch_graph_json(f"/graph/node/{node_type}")


def get_node_by_element_id(uid: str) -> object:
    uid_encoded = parse.quote(uid, safe="")
    return fetch_graph_json(f"/graph/node/elementId/{uid_encoded}")


def get_model(model_id: str) -> object:
    model_id_encoded = parse.quote(model_id, safe="")
    return fetch_graph_json(f"/cobra/model/{model_id_encoded}")


def infer_model_reaction_annotation(model_id: str, reaction_eid: str) -> object:
    model_id_encoded = parse.quote(model_id, safe="")
    reaction_eid_encoded = parse.quote(reaction_eid, safe="")
    return request_graph_json(
        f"/cobra/model/{model_id_encoded}/reaction/eid/{reaction_eid_encoded}/inference",
        method="POST",
        data=b"",
    )


def infer_model_all_reaction_annotation(model_id: str) -> object:
    model_id_encoded = parse.quote(model_id, safe="")
    return request_graph_json(
        f"/cobra/model/{model_id_encoded}/reaction/all/inference",
        method="POST",
        data=b"",
    )


def list_model_children(model_id: str, edge_type: str, node_type: str = NODE_TYPE_SBML_MODEL) -> object:
    model_id_encoded = parse.quote(model_id, safe="")
    return fetch_graph_json(
        f"/graph/node/{node_type}/{model_id_encoded}/child",
        query={"edgeType": edge_type},
    )


def list_node_children_by_eid(node_eid: str, edge_type: str) -> object:
    """
    This implementation does not exist in the SBML API. I need to be swapped later with a correct url
    """
    node_eid_encoded = parse.quote(node_eid, safe="")
    return fetch_graph_json(
        f"/graph/node/{node_eid_encoded}/child",
        query={"edgeType": edge_type},
    )

def list_node_children(node_type, node_key, edge_type) -> object:
    node_key_encoded = parse.quote(node_key, safe="")
    return fetch_graph_json(
        f"/graph/node/{node_type}/{node_key_encoded}/child",
        query={"edgeType": edge_type},
    )

def add_curation_event(subject_eid: str, object: str, agent_id: str, method: str, comment: str) -> object:
    subject_eid_encoded = parse.quote(subject_eid, safe="")
    object_eid_encoded = parse.quote(object, safe="")
    return request_graph_json(
        f"/graph/edge/{subject_eid_encoded}/{object_eid_encoded}/{EDGE_HAS_ANNOTATION_EVENT}",
        method="POST",
        json_body={"agent": agent_id, "method": method, "comment": comment},
    )

def list_curation_events_by_eid(subject_eid: str) -> object:
    return list_node_children_by_eid(subject_eid, EDGE_HAS_ANNOTATION_EVENT)


def list_curation_events(node_type: str, node_key: str) -> object:
    return list_node_children(node_type, node_key, EDGE_HAS_ANNOTATION_EVENT)
