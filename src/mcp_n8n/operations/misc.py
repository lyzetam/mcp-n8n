"""Miscellaneous operations — users, webhooks, status."""

from __future__ import annotations

from typing import Optional

from ..client import N8nClient


def list_users(
    client: N8nClient,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> dict:
    """List all users (admin only)."""
    params: dict = {"limit": limit}
    if cursor:
        params["cursor"] = cursor

    result = client.get("/users", params=params)
    users = result.get("data", result) if isinstance(result, dict) else result
    if not isinstance(users, list):
        users = [users]
    formatted = [
        {
            "id": u.get("id"),
            "email": u.get("email"),
            "firstName": u.get("firstName"),
            "lastName": u.get("lastName"),
            "role": u.get("role"),
            "createdAt": u.get("createdAt"),
        }
        for u in users
    ]
    return {
        "users": formatted,
        "nextCursor": result.get("nextCursor") if isinstance(result, dict) else None,
    }


def trigger_webhook(
    client: N8nClient,
    webhook_path: str,
    method: str = "POST",
    data: Optional[dict] = None,
    query_params: Optional[dict] = None,
) -> dict:
    """Trigger a webhook endpoint."""
    return client.webhook(webhook_path, method=method, json=data, params=query_params)


def status(client: N8nClient) -> dict:
    """Check n8n connection status and API availability."""
    try:
        client.get("/workflows", params={"limit": 1})
    except Exception as e:
        return {
            "status": "error",
            "host": client.base_url,
            "error": str(e),
        }

    try:
        active_result = client.get("/active-workflows")
        active_count = len(active_result) if isinstance(active_result, list) else 0
    except Exception:
        active_count = 0

    return {
        "status": "connected",
        "host": client.base_url,
        "active_workflows": active_count,
    }
