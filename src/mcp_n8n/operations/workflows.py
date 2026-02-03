"""Workflow operations — list, get, create, update, delete, activate, deactivate, execute, list_active."""

from __future__ import annotations

from typing import Optional

from ..client import N8nClient


def list_workflows(
    client: N8nClient,
    active: Optional[bool] = None,
    tags: Optional[str] = None,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> dict:
    """List all workflows with optional filtering."""
    params: dict = {"limit": limit}
    if active is not None:
        params["active"] = str(active).lower()
    if tags:
        params["tags"] = tags
    if cursor:
        params["cursor"] = cursor

    result = client.get("/workflows", params=params)
    workflows = result.get("data", result) if isinstance(result, dict) else result
    if not isinstance(workflows, list):
        workflows = [workflows]
    formatted = [
        {
            "id": wf.get("id"),
            "name": wf.get("name"),
            "active": wf.get("active"),
            "tags": [t.get("name") for t in wf.get("tags", [])],
            "createdAt": wf.get("createdAt"),
            "updatedAt": wf.get("updatedAt"),
        }
        for wf in workflows
    ]
    return {
        "workflows": formatted,
        "nextCursor": result.get("nextCursor") if isinstance(result, dict) else None,
    }


def get_workflow(client: N8nClient, workflow_id: str) -> dict:
    """Get detailed information about a specific workflow."""
    return client.get(f"/workflows/{workflow_id}")


def create_workflow(
    client: N8nClient,
    name: str,
    nodes: list,
    connections: dict,
    settings: Optional[dict] = None,
    static_data: Optional[dict] = None,
) -> dict:
    """Create a new workflow."""
    data: dict = {"name": name, "nodes": nodes, "connections": connections}
    if settings:
        data["settings"] = settings
    if static_data:
        data["staticData"] = static_data
    return client.post("/workflows", json=data)


def update_workflow(
    client: N8nClient,
    workflow_id: str,
    name: Optional[str] = None,
    nodes: Optional[list] = None,
    connections: Optional[dict] = None,
    settings: Optional[dict] = None,
    active: Optional[bool] = None,
) -> dict:
    """Update an existing workflow."""
    data: dict = {}
    if name is not None:
        data["name"] = name
    if nodes is not None:
        data["nodes"] = nodes
    if connections is not None:
        data["connections"] = connections
    if settings is not None:
        data["settings"] = settings
    if active is not None:
        data["active"] = active
    return client.put(f"/workflows/{workflow_id}", json=data)


def delete_workflow(client: N8nClient, workflow_id: str) -> dict:
    """Delete a workflow."""
    client.delete(f"/workflows/{workflow_id}")
    return {"status": "deleted", "workflow_id": workflow_id}


def activate_workflow(client: N8nClient, workflow_id: str) -> dict:
    """Activate a workflow to enable its triggers."""
    client.post(f"/workflows/{workflow_id}/activate")
    return {"id": workflow_id, "active": True, "message": "Workflow activated successfully"}


def deactivate_workflow(client: N8nClient, workflow_id: str) -> dict:
    """Deactivate a workflow to disable its triggers."""
    client.post(f"/workflows/{workflow_id}/deactivate")
    return {"id": workflow_id, "active": False, "message": "Workflow deactivated successfully"}


def execute_workflow(client: N8nClient, workflow_id: str, data: Optional[dict] = None) -> dict:
    """Execute a workflow manually with optional input data."""
    payload = {}
    if data:
        payload["data"] = data
    return client.post(f"/workflows/{workflow_id}/run", json=payload if payload else None)


def list_active_workflows(client: N8nClient) -> list:
    """List all currently active workflow IDs."""
    result = client.get("/active-workflows")
    return result if isinstance(result, list) else [result]


def get_activation_error(client: N8nClient, workflow_id: str) -> dict:
    """Get activation error for a specific workflow."""
    return client.get(f"/active-workflows/error/{workflow_id}")
