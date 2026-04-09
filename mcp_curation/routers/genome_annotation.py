from fastapi import APIRouter, HTTPException, Path

from mcp_curation.client import sbml_client

router = APIRouter(prefix="/genome-annotation", tags=["genome-annotation"])

NODE_TYPE_GENOME = "Genome"
NODE_TYPE_GENOMIC_CONTIG = "GenomicContig"
EDGE_HAS_FEATURE = "has_feature"
EDGE_HAS_CONTIG = "has_contig"

_GENOME_ID = Path(example="GCF_000046845.1")


def _handle_sbml_error(exc: sbml_client.SBMLApiError) -> None:
    raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc


@router.get("/genome")
def list_genomes() -> object:
    try:
        return sbml_client.fetch_graph_json(f"/graph/node/{NODE_TYPE_GENOME}")
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/genome/{genome_id}/features")
def list_genome_features(genome_id: str = _GENOME_ID) -> object:
    try:
        contigs = sbml_client.list_node_children(NODE_TYPE_GENOME, genome_id, EDGE_HAS_CONTIG)
        features = []
        for row in contigs:

            contig_node = row[1] if isinstance(row, list) and len(row) > 1 else None
            if isinstance(contig_node, dict):
                contig_key = contig_node.get("entry")
                if contig_key:
                    contig_features = sbml_client.list_node_children(
                        NODE_TYPE_GENOMIC_CONTIG, contig_key, EDGE_HAS_FEATURE
                    )
                    features.extend(contig_features)
        return features
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)


@router.get("/genome/{genome_id}/contigs")
def list_genome_contigs(genome_id: str = _GENOME_ID) -> object:
    try:
        return sbml_client.list_node_children(NODE_TYPE_GENOME, genome_id, EDGE_HAS_CONTIG)
    except sbml_client.SBMLApiError as exc:
        _handle_sbml_error(exc)
