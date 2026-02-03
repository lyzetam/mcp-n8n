"""n8n MCP Server — backward-compatible @mcp.tool wrappers.

Tool names match the original server.py for drop-in replacement.
"""

from __future__ import annotations

import json
from typing import Optional

from fastmcp import FastMCP

from .client import N8nClient
from .operations import credentials, executions, misc, tags, workflows

mcp = FastMCP("n8n-mcp")

_client: N8nClient | None = None


def _get_client() -> N8nClient:
    global _client
    if _client is None:
        _client = N8nClient()
    return _client


# --- Workflows ---

@mcp.tool
def n8n_list_workflows(
    active: Optional[bool] = None,
    tags: Optional[str] = None,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> str:
    """List all workflows with optional filtering."""
    return json.dumps(
        workflows.list_workflows(
            _get_client(), active=active, tags=tags, limit=limit, cursor=cursor,
        ),
        indent=2,
    )


@mcp.tool
def n8n_get_workflow(workflow_id: str) -> str:
    """Get detailed information about a specific workflow."""
    return json.dumps(workflows.get_workflow(_get_client(), workflow_id), indent=2)


@mcp.tool
def n8n_create_workflow(
    name: str,
    nodes: list,
    connections: dict,
    settings: Optional[dict] = None,
    static_data: Optional[dict] = None,
) -> str:
    """Create a new workflow."""
    return json.dumps(
        workflows.create_workflow(
            _get_client(), name, nodes, connections,
            settings=settings, static_data=static_data,
        ),
        indent=2,
    )


@mcp.tool
def n8n_update_workflow(
    workflow_id: str,
    name: Optional[str] = None,
    nodes: Optional[list] = None,
    connections: Optional[dict] = None,
    settings: Optional[dict] = None,
    active: Optional[bool] = None,
) -> str:
    """Update an existing workflow."""
    return json.dumps(
        workflows.update_workflow(
            _get_client(), workflow_id,
            name=name, nodes=nodes, connections=connections,
            settings=settings, active=active,
        ),
        indent=2,
    )


@mcp.tool
def n8n_delete_workflow(workflow_id: str) -> str:
    """Delete a workflow."""
    return json.dumps(workflows.delete_workflow(_get_client(), workflow_id), indent=2)


@mcp.tool
def n8n_activate_workflow(workflow_id: str) -> str:
    """Activate a workflow to enable its triggers."""
    return json.dumps(workflows.activate_workflow(_get_client(), workflow_id), indent=2)


@mcp.tool
def n8n_deactivate_workflow(workflow_id: str) -> str:
    """Deactivate a workflow to disable its triggers."""
    return json.dumps(workflows.deactivate_workflow(_get_client(), workflow_id), indent=2)


@mcp.tool
def n8n_execute_workflow(workflow_id: str, data: Optional[dict] = None) -> str:
    """Execute a workflow manually with optional input data."""
    return json.dumps(workflows.execute_workflow(_get_client(), workflow_id, data=data), indent=2)


@mcp.tool
def n8n_list_active_workflows() -> str:
    """List all currently active workflow IDs."""
    return json.dumps(workflows.list_active_workflows(_get_client()), indent=2)


@mcp.tool
def n8n_get_activation_error(workflow_id: str) -> str:
    """Get activation error for a specific workflow."""
    return json.dumps(workflows.get_activation_error(_get_client(), workflow_id), indent=2)


# --- Executions ---

@mcp.tool
def n8n_list_executions(
    workflow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    cursor: Optional[str] = None,
) -> str:
    """List workflow executions with optional filtering."""
    return json.dumps(
        executions.list_executions(
            _get_client(), workflow_id=workflow_id, status=status, limit=limit, cursor=cursor,
        ),
        indent=2,
    )


@mcp.tool
def n8n_get_execution(execution_id: str, include_data: bool = False) -> str:
    """Get detailed information about a specific execution."""
    return json.dumps(
        executions.get_execution(_get_client(), execution_id, include_data=include_data),
        indent=2,
    )


@mcp.tool
def n8n_delete_execution(execution_id: str) -> str:
    """Delete an execution."""
    return json.dumps(executions.delete_execution(_get_client(), execution_id), indent=2)


@mcp.tool
def n8n_retry_execution(execution_id: str) -> str:
    """Retry a failed execution."""
    return json.dumps(executions.retry_execution(_get_client(), execution_id), indent=2)


@mcp.tool
def n8n_stop_execution(execution_id: str) -> str:
    """Stop a running execution."""
    return json.dumps(executions.stop_execution(_get_client(), execution_id), indent=2)


# --- Credentials ---

@mcp.tool
def n8n_list_credentials(limit: int = 100, cursor: Optional[str] = None) -> str:
    """List all credentials (without sensitive data)."""
    return json.dumps(
        credentials.list_credentials(_get_client(), limit=limit, cursor=cursor),
        indent=2,
    )


@mcp.tool
def n8n_get_credential_schema(credential_type: str) -> str:
    """Get the schema for a credential type."""
    return json.dumps(credentials.get_credential_schema(_get_client(), credential_type), indent=2)


@mcp.tool
def n8n_create_credential(name: str, credential_type: str, data: dict) -> str:
    """Create a new credential."""
    return json.dumps(
        credentials.create_credential(_get_client(), name, credential_type, data),
        indent=2,
    )


@mcp.tool
def n8n_delete_credential(credential_id: str) -> str:
    """Delete a credential."""
    return json.dumps(credentials.delete_credential(_get_client(), credential_id), indent=2)


# --- Tags ---

@mcp.tool
def n8n_list_tags(limit: int = 100, cursor: Optional[str] = None) -> str:
    """List all tags."""
    return json.dumps(tags.list_tags(_get_client(), limit=limit, cursor=cursor), indent=2)


@mcp.tool
def n8n_create_tag(name: str) -> str:
    """Create a new tag."""
    return json.dumps(tags.create_tag(_get_client(), name), indent=2)


@mcp.tool
def n8n_delete_tag(tag_id: str) -> str:
    """Delete a tag."""
    return json.dumps(tags.delete_tag(_get_client(), tag_id), indent=2)


# --- Users ---

@mcp.tool
def n8n_list_users(limit: int = 100, cursor: Optional[str] = None) -> str:
    """List all users (admin only)."""
    return json.dumps(misc.list_users(_get_client(), limit=limit, cursor=cursor), indent=2)


# --- Webhooks ---

@mcp.tool
def n8n_trigger_webhook(
    webhook_path: str,
    method: str = "POST",
    data: Optional[dict] = None,
    query_params: Optional[dict] = None,
) -> str:
    """Trigger a webhook endpoint."""
    return json.dumps(
        misc.trigger_webhook(
            _get_client(), webhook_path, method=method, data=data, query_params=query_params,
        ),
        indent=2,
    )


# --- Status ---

@mcp.tool
def n8n_status() -> str:
    """Check n8n connection status and API availability."""
    return json.dumps(misc.status(_get_client()), indent=2)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
