import requests

DEFAULT_BASE_URL = "http://localhost:8000"


class MCPClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL, api_key: str = ""):
        self._base_url = base_url.rstrip("/")
        self._session = requests.Session()
        if api_key:
            self._session.headers["X-API-Key"] = api_key

    def _get(self, path: str, **params) -> object:
        response = self._session.get(f"{self._base_url}{path}", params=params or None)
        response.raise_for_status()
        return response.json()

    def _post(self, path: str, json: dict | None = None) -> object:
        response = self._session.post(f"{self._base_url}{path}", json=json)
        response.raise_for_status()
        return response.json()

    # --- sbml-curation ---

    def sbml_config(self) -> object:
        return self._get("/sbml-curation/config")

    def list_models(self, model_type: str = "sbml") -> object:
        return self._get("/sbml-curation/models", model_type=model_type)

    def get_model(self, model_id: str, model_type: str = "sbml") -> object:
        return self._get(f"/sbml-curation/models/{model_id}", model_type=model_type)

    def list_model_compartments(self, model_id: str, model_type: str = "sbml") -> object:
        return self._get(f"/sbml-curation/models/{model_id}/compartments", model_type=model_type)

    def list_model_species(self, model_id: str, model_type: str = "sbml") -> object:
        return self._get(f"/sbml-curation/models/{model_id}/species", model_type=model_type)

    def list_model_reactions(self, model_id: str, model_type: str = "sbml") -> object:
        return self._get(f"/sbml-curation/models/{model_id}/reactions", model_type=model_type)

    def list_model_genes(self, model_id: str, model_type: str = "sbml") -> object:
        return self._get(f"/sbml-curation/models/{model_id}/genes", model_type=model_type)

    def add_annotation(
        self,
        subject_eid: str,
        object: str,
        agent_id: str,
        method: str,
        comment: str,
    ) -> object:
        return self._post(
            "/sbml-curation/annotation",
            json={
                "subject_eid": subject_eid,
                "object": object,
                "agent_id": agent_id,
                "method": method,
                "comment": comment,
            },
        )

    def list_compartment_annotation(self, model_id: str, compartment_id: str) -> object:
        return self._get(f"/sbml-curation/models/{model_id}/compartment/{compartment_id}/annotation")

    def list_species_annotation(self, model_id: str, species_id: str) -> object:
        return self._get(f"/sbml-curation/models/{model_id}/species/{species_id}/annotation")

    def list_reaction_annotation(self, model_id: str, reaction_id: str) -> object:
        return self._get(f"/sbml-curation/models/{model_id}/reaction/{reaction_id}/annotation")

    def list_gene_annotation(self, model_id: str, gene_id: str) -> object:
        return self._get(f"/sbml-curation/models/{model_id}/gene/{gene_id}/annotation")

    def infer_reaction_annotation(self, model_id: str, reaction_eid: str) -> object:
        return self._post(f"/sbml-curation/models/{model_id}/reaction/{reaction_eid}/inference")

    def infer_all_reaction_annotations(self, model_id: str) -> object:
        return self._post(f"/sbml-curation/models/{model_id}/reaction/inference")

    # --- genome-annotation ---

    def list_genomes(self) -> object:
        return self._get("/genome-annotation/genome")

    def list_genome_contigs(self, genome_id: str) -> object:
        return self._get(f"/genome-annotation/genome/{genome_id}/contigs")

    def list_genome_features(self, genome_id: str) -> object:
        return self._get(f"/genome-annotation/genome/{genome_id}/features")
