"""LangChain @tool wrappers for n8n operations.

Usage:
    from mcp_n8n.langchain_tools import TOOLS

    # Or import individual tools:
    from mcp_n8n.langchain_tools import n8n_list_workflows, n8n_execute_workflow
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Optional

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from .client import N8nClient
from .operations import credentials, executions, misc, tags, workflows


@lru_cache
def _get_client() -> N8nClient:
    """Singleton N8nClient configured from environment."""
    return N8nClient()


# =============================================================================
# Workflows
# =============================================================================


class ListWorkflowsInput(BaseModel):
    active: Optional[bool] = Field(default=None, description="Filter by active status (True/False)")
    tags: Optional[str] = Field(default=None, description="Comma-separated list of tag IDs to filter by")
    limit: int = Field(default=100, description="Maximum number of workflows to return")
    cursor: Optional[str] = Field(default=None, description="Cursor for pagination")


@tool(args_schema=ListWorkflowsInput)
def n8n_list_workflows(
    active: Optional[bool] = None,
    tags: Optional[str] = None,
    limit: int = 100,
    cursor: Optional[str] = None,
) -> str:
    """List all n8n workflows with optional filtering."""
    return json.dumps(
        workflows.list_workflows(
            _get_client(), active=active, tags=tags, limit=limit, cursor=cursor,
        ),
        indent=2,
    )


class GetWorkflowInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow to retrieve")


@tool(args_schema=GetWorkflowInput)
def n8n_get_workflow(workflow_id: str) -> str:
    """Get detailed information about a specific n8n workflow."""
    return json.dumps(workflows.get_workflow(_get_client(), workflow_id), indent=2)


class CreateWorkflowInput(BaseModel):
    name: str = Field(description="Name of the workflow")
    nodes: list = Field(description="List of node objects defining the workflow")
    connections: dict = Field(description="Connection definitions between nodes")
    settings: Optional[dict] = Field(default=None, description="Optional workflow settings")
    static_data: Optional[dict] = Field(default=None, description="Optional static data for the workflow")


@tool(args_schema=CreateWorkflowInput)
def n8n_create_workflow(
    name: str,
    nodes: list,
    connections: dict,
    settings: Optional[dict] = None,
    static_data: Optional[dict] = None,
) -> str:
    """Create a new n8n workflow."""
    return json.dumps(
        workflows.create_workflow(
            _get_client(), name, nodes, connections,
            settings=settings, static_data=static_data,
        ),
        indent=2,
    )


class UpdateWorkflowInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow to update")
    name: Optional[str] = Field(default=None, description="New name for the workflow")
    nodes: Optional[list] = Field(default=None, description="Updated list of nodes")
    connections: Optional[dict] = Field(default=None, description="Updated connections")
    settings: Optional[dict] = Field(default=None, description="Updated settings")
    active: Optional[bool] = Field(default=None, description="Set workflow active status")


@tool(args_schema=UpdateWorkflowInput)
def n8n_update_workflow(
    workflow_id: str,
    name: Optional[str] = None,
    nodes: Optional[list] = None,
    connections: Optional[dict] = None,
    settings: Optional[dict] = None,
    active: Optional[bool] = None,
) -> str:
    """Update an existing n8n workflow."""
    return json.dumps(
        workflows.update_workflow(
            _get_client(), workflow_id,
            name=name, nodes=nodes, connections=connections,
            settings=settings, active=active,
        ),
        indent=2,
    )


class DeleteWorkflowInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow to delete")


@tool(args_schema=DeleteWorkflowInput)
def n8n_delete_workflow(workflow_id: str) -> str:
    """Delete an n8n workflow."""
    return json.dumps(workflows.delete_workflow(_get_client(), workflow_id), indent=2)


class ActivateWorkflowInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow to activate")


@tool(args_schema=ActivateWorkflowInput)
def n8n_activate_workflow(workflow_id: str) -> str:
    """Activate an n8n workflow to enable its triggers."""
    return json.dumps(workflows.activate_workflow(_get_client(), workflow_id), indent=2)


class DeactivateWorkflowInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow to deactivate")


@tool(args_schema=DeactivateWorkflowInput)
def n8n_deactivate_workflow(workflow_id: str) -> str:
    """Deactivate an n8n workflow to disable its triggers."""
    return json.dumps(workflows.deactivate_workflow(_get_client(), workflow_id), indent=2)


class ExecuteWorkflowInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow to execute")
    data: Optional[dict] = Field(default=None, description="Optional input data to pass to the workflow")


@tool(args_schema=ExecuteWorkflowInput)
def n8n_execute_workflow(workflow_id: str, data: Optional[dict] = None) -> str:
    """Execute an n8n workflow manually with optional input data."""
    return json.dumps(workflows.execute_workflow(_get_client(), workflow_id, data=data), indent=2)


@tool
def n8n_list_active_workflows() -> str:
    """List all currently active n8n workflow IDs."""
    return json.dumps(workflows.list_active_workflows(_get_client()), indent=2)


class GetActivationErrorInput(BaseModel):
    workflow_id: str = Field(description="The ID of the workflow")


@tool(args_schema=GetActivationErrorInput)
def n8n_get_activation_error(workflow_id: str) -> str:
    """Get activation error for a specific n8n workflow."""
    return json.dumps(workflows.get_activation_error(_get_client(), workflow_id), indent=2)


# =============================================================================
# Executions
# =============================================================================


class ListExecutionsInput(BaseModel):
    workflow_id: Optional[str] = Field(default=None, description="Filter by workflow ID")
    status: Optional[str] = Field(default=None, description="Filter by status (waiting, running, success, error)")
    limit: int = Field(default=20, description="Maximum number of executions to return")
    cursor: Optional[str] = Field(default=None, description="Cursor for pagination")


@tool(args_schema=ListExecutionsInput)
def n8n_list_executions(
    workflow_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 20,
    cursor: Optional[str] = None,
) -> str:
    """List n8n workflow executions with optional filtering."""
    return json.dumps(
        executions.list_executions(
            _get_client(), workflow_id=workflow_id, status=status, limit=limit, cursor=cursor,
        ),
        indent=2,
    )


class GetExecutionInput(BaseModel):
    execution_id: str = Field(description="The ID of the execution to retrieve")
    include_data: bool = Field(default=False, description="Include execution data in the response")


@tool(args_schema=GetExecutionInput)
def n8n_get_execution(execution_id: str, include_data: bool = False) -> str:
    """Get detailed information about a specific n8n execution."""
    return json.dumps(
        executions.get_execution(_get_client(), execution_id, include_data=include_data),
        indent=2,
    )


class DeleteExecutionInput(BaseModel):
    execution_id: str = Field(description="The ID of the execution to delete")


@tool(args_schema=DeleteExecutionInput)
def n8n_delete_execution(execution_id: str) -> str:
    """Delete an n8n execution."""
    return json.dumps(executions.delete_execution(_get_client(), execution_id), indent=2)


class RetryExecutionInput(BaseModel):
    execution_id: str = Field(description="The ID of the execution to retry")


@tool(args_schema=RetryExecutionInput)
def n8n_retry_execution(execution_id: str) -> str:
    """Retry a failed n8n execution."""
    return json.dumps(executions.retry_execution(_get_client(), execution_id), indent=2)


class StopExecutionInput(BaseModel):
    execution_id: str = Field(description="The ID of the execution to stop")


@tool(args_schema=StopExecutionInput)
def n8n_stop_execution(execution_id: str) -> str:
    """Stop a running n8n execution."""
    return json.dumps(executions.stop_execution(_get_client(), execution_id), indent=2)


# =============================================================================
# Credentials
# =============================================================================


class ListCredentialsInput(BaseModel):
    limit: int = Field(default=100, description="Maximum number of credentials to return")
    cursor: Optional[str] = Field(default=None, description="Cursor for pagination")


@tool(args_schema=ListCredentialsInput)
def n8n_list_credentials(limit: int = 100, cursor: Optional[str] = None) -> str:
    """List all n8n credentials (without sensitive data)."""
    return json.dumps(
        credentials.list_credentials(_get_client(), limit=limit, cursor=cursor),
        indent=2,
    )


class GetCredentialSchemaInput(BaseModel):
    credential_type: str = Field(description="The type of credential (e.g., 'slackApi', 'githubApi')")


@tool(args_schema=GetCredentialSchemaInput)
def n8n_get_credential_schema(credential_type: str) -> str:
    """Get the schema for an n8n credential type."""
    return json.dumps(credentials.get_credential_schema(_get_client(), credential_type), indent=2)


class CreateCredentialInput(BaseModel):
    name: str = Field(description="Name for the credential")
    credential_type: str = Field(description="Type of credential (e.g., 'slackApi')")
    data: dict = Field(description="Credential data (API keys, tokens, etc.)")


@tool(args_schema=CreateCredentialInput)
def n8n_create_credential(name: str, credential_type: str, data: dict) -> str:
    """Create a new n8n credential."""
    return json.dumps(
        credentials.create_credential(_get_client(), name, credential_type, data),
        indent=2,
    )


class DeleteCredentialInput(BaseModel):
    credential_id: str = Field(description="The ID of the credential to delete")


@tool(args_schema=DeleteCredentialInput)
def n8n_delete_credential(credential_id: str) -> str:
    """Delete an n8n credential."""
    return json.dumps(credentials.delete_credential(_get_client(), credential_id), indent=2)


# =============================================================================
# Tags
# =============================================================================


class ListTagsInput(BaseModel):
    limit: int = Field(default=100, description="Maximum number of tags to return")
    cursor: Optional[str] = Field(default=None, description="Cursor for pagination")


@tool(args_schema=ListTagsInput)
def n8n_list_tags(limit: int = 100, cursor: Optional[str] = None) -> str:
    """List all n8n tags."""
    return json.dumps(tags.list_tags(_get_client(), limit=limit, cursor=cursor), indent=2)


class CreateTagInput(BaseModel):
    name: str = Field(description="Name for the tag")


@tool(args_schema=CreateTagInput)
def n8n_create_tag(name: str) -> str:
    """Create a new n8n tag."""
    return json.dumps(tags.create_tag(_get_client(), name), indent=2)


class DeleteTagInput(BaseModel):
    tag_id: str = Field(description="The ID of the tag to delete")


@tool(args_schema=DeleteTagInput)
def n8n_delete_tag(tag_id: str) -> str:
    """Delete an n8n tag."""
    return json.dumps(tags.delete_tag(_get_client(), tag_id), indent=2)


# =============================================================================
# Misc
# =============================================================================


class ListUsersInput(BaseModel):
    limit: int = Field(default=100, description="Maximum number of users to return")
    cursor: Optional[str] = Field(default=None, description="Cursor for pagination")


@tool(args_schema=ListUsersInput)
def n8n_list_users(limit: int = 100, cursor: Optional[str] = None) -> str:
    """List all n8n users (admin only)."""
    return json.dumps(misc.list_users(_get_client(), limit=limit, cursor=cursor), indent=2)


class TriggerWebhookInput(BaseModel):
    webhook_path: str = Field(description="The webhook path (without /webhook/ prefix)")
    method: str = Field(default="POST", description="HTTP method (GET, POST, PUT, DELETE)")
    data: Optional[dict] = Field(default=None, description="Request body data (for POST/PUT)")
    query_params: Optional[dict] = Field(default=None, description="Query parameters")


@tool(args_schema=TriggerWebhookInput)
def n8n_trigger_webhook(
    webhook_path: str,
    method: str = "POST",
    data: Optional[dict] = None,
    query_params: Optional[dict] = None,
) -> str:
    """Trigger an n8n webhook endpoint."""
    return json.dumps(
        misc.trigger_webhook(
            _get_client(), webhook_path, method=method, data=data, query_params=query_params,
        ),
        indent=2,
    )


@tool
def n8n_status() -> str:
    """Check n8n connection status and API availability."""
    return json.dumps(misc.status(_get_client()), indent=2)


# =============================================================================
# Tool exports
# =============================================================================

TOOLS = [
    # Workflows
    n8n_list_workflows,
    n8n_get_workflow,
    n8n_create_workflow,
    n8n_update_workflow,
    n8n_delete_workflow,
    n8n_activate_workflow,
    n8n_deactivate_workflow,
    n8n_execute_workflow,
    n8n_list_active_workflows,
    n8n_get_activation_error,
    # Executions
    n8n_list_executions,
    n8n_get_execution,
    n8n_delete_execution,
    n8n_retry_execution,
    n8n_stop_execution,
    # Credentials
    n8n_list_credentials,
    n8n_get_credential_schema,
    n8n_create_credential,
    n8n_delete_credential,
    # Tags
    n8n_list_tags,
    n8n_create_tag,
    n8n_delete_tag,
    # Misc
    n8n_list_users,
    n8n_trigger_webhook,
    n8n_status,
]
