"""Execution operations — list, get, delete, retry, stop."""

from __future__ import annotations

from typing import Optional

from ..client import N8nClient


def list_executions(
    client: N8nClient,
    workflow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    cursor: Optional[str] = None,
) -> dict:
    """List workflow executions with optional filtering."""
    params: dict = {"limit": limit}
    if workflow_id:
        params["workflowId"] = workflow_id
    if status:
        params["status"] = status
    if cursor:
        params["cursor"] = cursor

    result = client.get("/executions", params=params)
    executions = result.get("data", result) if isinstance(result, dict) else result
    if not isinstance(executions, list):
        executions = [executions]
    formatted = [
        {
            "id": ex.get("id"),
            "workflowId": ex.get("workflowId"),
            "workflowName": ex.get("workflowData", {}).get("name") if ex.get("workflowData") else None,
            "status": ex.get("status"),
            "mode": ex.get("mode"),
            "startedAt": ex.get("startedAt"),
            "stoppedAt": ex.get("stoppedAt"),
            "finished": ex.get("finished"),
        }
        for ex in executions
    ]
    return {
        "executions": formatted,
        "nextCursor": result.get("nextCursor") if isinstance(result, dict) else None,
    }


def get_execution(client: N8nClient, execution_id: str, include_data: bool = False) -> dict:
    """Get detailed information about a specific execution."""
    params = {}
    if include_data:
        params["includeData"] = "true"
    return client.get(f"/executions/{execution_id}", params=params or None)


def delete_execution(client: N8nClient, execution_id: str) -> dict:
    """Delete an execution."""
    client.delete(f"/executions/{execution_id}")
    return {"status": "deleted", "execution_id": execution_id}


def retry_execution(client: N8nClient, execution_id: str) -> dict:
    """Retry a failed execution."""
    return client.post(f"/executions/{execution_id}/retry")


def stop_execution(client: N8nClient, execution_id: str) -> dict:
    """Stop a running execution."""
    client.post(f"/executions/{execution_id}/stop")
    return {"id": execution_id, "message": "Execution stopped"}
