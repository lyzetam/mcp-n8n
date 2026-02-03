"""Tag operations — list, create, delete."""

from __future__ import annotations

from typing import Optional

from ..client import N8nClient


def list_tags(
    client: N8nClient,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> dict:
    """List all tags."""
    params: dict = {"limit": limit}
    if cursor:
        params["cursor"] = cursor

    result = client.get("/tags", params=params)
    tags = result.get("data", result) if isinstance(result, dict) else result
    if not isinstance(tags, list):
        tags = [tags]
    formatted = [
        {
            "id": tag.get("id"),
            "name": tag.get("name"),
            "createdAt": tag.get("createdAt"),
            "updatedAt": tag.get("updatedAt"),
        }
        for tag in tags
    ]
    return {
        "tags": formatted,
        "nextCursor": result.get("nextCursor") if isinstance(result, dict) else None,
    }


def create_tag(client: N8nClient, name: str) -> dict:
    """Create a new tag."""
    return client.post("/tags", json={"name": name})


def delete_tag(client: N8nClient, tag_id: str) -> dict:
    """Delete a tag."""
    client.delete(f"/tags/{tag_id}")
    return {"status": "deleted", "tag_id": tag_id}
