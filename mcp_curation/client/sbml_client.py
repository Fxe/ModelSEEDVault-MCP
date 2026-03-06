import json
import os
from urllib import error, parse, request

DEFAULT_SBML_API_BASE_URL = "http://192.168.1.202:8080"
REQUEST_TIMEOUT_SECONDS = 20
NODE_TYPE_SBML_MODEL = "SBMLModel"
EDGE_HAS_COMPARTMENT = "has_sbml_compartment"
EDGE_HAS_SPECIES = "has_sbml_species"
EDGE_HAS_REACTION = "has_sbml_reaction"
EDGE_HAS_GENE = "has_sbml_gene"


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


def fetch_graph_json(path: str, query: dict[str, str] | None = None) -> object:
    query_string = f"?{parse.urlencode(query)}" if query else ""
    url = f"{api_base_url()}{path}{query_string}"
    req = request.Request(url=url, headers={"accept": "*/*"})

    try:
        with request.urlopen(req, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else {}
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
    except json.JSONDecodeError as exc:
        raise SBMLApiError(
            status_code=502,
            detail="SBML API returned non-JSON response",
        ) from exc


def list_models() -> object:
    return fetch_graph_json(f"/graph/node/{NODE_TYPE_SBML_MODEL}")


def list_model_children(model_id: str, edge_type: str) -> object:
    model_id_encoded = parse.quote(model_id, safe="")
    return fetch_graph_json(
        f"/graph/node/{NODE_TYPE_SBML_MODEL}/{model_id_encoded}/child",
        query={"edgeType": edge_type},
    )

