"""Thin wrapper around graph_data for API responses."""
from typing import List, Dict, Optional

from app import graph_data


def get_domains() -> List[Dict]:
    """Return all available domains."""
    domains = graph_data.get_all_domains()
    result = []
    for d in domains:
        result.append({
            "id": d["id"],
            "name": d["name"],
            "description": d["description"],
            "total_knowledge_points": graph_data.count_nodes_in_domain(d["id"]),
        })
    return result


def get_domain_map(domain_id: str) -> Optional[Dict]:
    """Return full map data for a domain."""
    node = graph_data.get_node(domain_id)
    if node is None or node.get("node_type") != "domain":
        return None
    return graph_data.get_domain_map(domain_id)


def get_node_detail(node_id: str) -> Optional[Dict]:
    """Return detailed info for a single node."""
    node = graph_data.get_node(node_id)
    if node is None:
        return None

    prerequisites = []
    for pid in graph_data.get_prerequisites(node_id):
        p = graph_data.get_node(pid)
        if p:
            prerequisites.append({"id": p["id"], "name": p["name"]})

    successors = []
    for sid in graph_data.get_successors(node_id):
        s = graph_data.get_node(sid)
        if s:
            successors.append({"id": s["id"], "name": s["name"]})

    related = []
    for rid in graph_data.get_related_nodes(node_id):
        r = graph_data.get_node(rid)
        if r:
            related.append({"id": r["id"], "name": r["name"]})

    return {
        **node,
        "prerequisites": prerequisites,
        "successors": successors,
        "related_nodes": related,
    }
