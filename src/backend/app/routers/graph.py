"""Graph router: public knowledge-graph endpoints."""
from fastapi import APIRouter, HTTPException

from app.services import graph_service

router = APIRouter()


@router.get("/domains")
def list_domains():
    """Return all available knowledge domains."""
    return graph_service.get_domains()


@router.get("/map/{domain_id}")
def get_domain_map(domain_id: str):
    """Return full graph data for a domain (nodes + edges)."""
    result = graph_service.get_domain_map(domain_id)
    if result is None:
        raise HTTPException(status_code=404, detail="域不存在")
    return result


@router.get("/node/{node_id}")
def get_node_detail(node_id: str):
    """Return details for a single node, including its relationships."""
    result = graph_service.get_node_detail(node_id)
    if result is None:
        raise HTTPException(status_code=404, detail="节点不存在")
    return result
