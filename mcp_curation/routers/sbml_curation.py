from fastapi import APIRouter

router = APIRouter(prefix="/sbml-curation", tags=["sbml-curation"])

_MODELS = [
    {"id": "msv_model_001", "name": "Example Core Metabolism"},
    {"id": "msv_model_002", "name": "Example Amino Acid Biosynthesis"},
]

_COMPARTMENTS_BY_MODEL = {
    "msv_model_001": [
        {"id": "c", "name": "cytosol"},
        {"id": "e", "name": "extracellular"},
    ],
    "msv_model_002": [
        {"id": "c", "name": "cytosol"},
    ],
}

_SPECIES_BY_MODEL = {
    "msv_model_001": [
        {"id": "cpd00001_c", "name": "Water"},
        {"id": "cpd00067_c", "name": "H+"},
    ],
    "msv_model_002": [
        {"id": "cpd00156_c", "name": "L-Valine"},
    ],
}

_REACTIONS_BY_MODEL = {
    "msv_model_001": [
        {"id": "rxn00001_c", "name": "ATP hydrolysis"},
        {"id": "rxn00002_c", "name": "NADH oxidation"},
    ],
    "msv_model_002": [
        {"id": "rxn00158_c", "name": "Valine transamination"},
    ],
}

_GENES_BY_MODEL = {
    "msv_model_001": [
        {"id": "geneA", "locus_tag": "MSV_0001"},
        {"id": "geneB", "locus_tag": "MSV_0002"},
    ],
    "msv_model_002": [
        {"id": "geneC", "locus_tag": "MSV_0100"},
    ],
}


@router.get("/models")
def list_models() -> dict[str, list[dict[str, str]]]:
    return {"models": _MODELS}


@router.get("/models/{model_id}/compartments")
def list_model_compartments(model_id: str) -> dict[str, object]:
    return {"model_id": model_id, "compartments": _COMPARTMENTS_BY_MODEL.get(model_id, [])}


@router.get("/models/{model_id}/species")
def list_model_species(model_id: str) -> dict[str, object]:
    return {"model_id": model_id, "species": _SPECIES_BY_MODEL.get(model_id, [])}


@router.get("/models/{model_id}/reactions")
def list_model_reactions(model_id: str) -> dict[str, object]:
    return {"model_id": model_id, "reactions": _REACTIONS_BY_MODEL.get(model_id, [])}


@router.get("/models/{model_id}/genes")
def list_model_genes(model_id: str) -> dict[str, object]:
    return {"model_id": model_id, "genes": _GENES_BY_MODEL.get(model_id, [])}

