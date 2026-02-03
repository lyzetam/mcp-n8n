"""Credential operations — list, get_schema, create, delete."""

from __future__ import annotations

from typing import Optional

from ..client import N8nClient


def list_credentials(
    client: N8nClient,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> dict:
    """List all credentials (without sensitive data)."""
    params: dict = {"limit": limit}
    if cursor:
        params["cursor"] = cursor

    result = client.get("/credentials", params=params)
    credentials = result.get("data", result) if isinstance(result, dict) else result
    if not isinstance(credentials, list):
        credentials = [credentials]
    formatted = [
        {
            "id": cred.get("id"),
            "name": cred.get("name"),
            "type": cred.get("type"),
            "createdAt": cred.get("createdAt"),
            "updatedAt": cred.get("updatedAt"),
        }
        for cred in credentials
    ]
    return {
        "credentials": formatted,
        "nextCursor": result.get("nextCursor") if isinstance(result, dict) else None,
    }


def get_credential_schema(client: N8nClient, credential_type: str) -> dict:
    """Get the schema for a credential type."""
    return client.get(f"/credentials/schema/{credential_type}")


def create_credential(client: N8nClient, name: str, credential_type: str, data: dict) -> dict:
    """Create a new credential."""
    payload = {"name": name, "type": credential_type, "data": data}
    return client.post("/credentials", json=payload)


def delete_credential(client: N8nClient, credential_id: str) -> dict:
    """Delete a credential."""
    client.delete(f"/credentials/{credential_id}")
    return {"status": "deleted", "credential_id": credential_id}
