"""Tests for n8n operations using responses mocks."""

import responses

from mcp_n8n.client import N8nClient
from mcp_n8n.operations import credentials, executions, misc, tags, workflows

BASE = "http://localhost:5678"
API = f"{BASE}/api/v1"


def _client():
    return N8nClient(base_url=BASE, api_key="test-key")


# =============================================================================
# Workflow operations
# =============================================================================


@responses.activate
def test_list_workflows():
    responses.get(f"{API}/workflows", json={
        "data": [
            {"id": "1", "name": "My Workflow", "active": True, "tags": [{"name": "prod"}], "createdAt": "2025-01-01", "updatedAt": "2025-01-02"}
        ],
        "nextCursor": None,
    })
    result = workflows.list_workflows(_client())
    assert len(result["workflows"]) == 1
    assert result["workflows"][0]["name"] == "My Workflow"
    assert result["workflows"][0]["tags"] == ["prod"]


@responses.activate
def test_list_workflows_with_filters():
    responses.get(f"{API}/workflows", json={"data": []})
    result = workflows.list_workflows(_client(), active=True, tags="tag1", limit=10)
    assert result["workflows"] == []


@responses.activate
def test_get_workflow():
    responses.get(f"{API}/workflows/1", json={"id": "1", "name": "My Workflow", "nodes": [], "connections": {}})
    result = workflows.get_workflow(_client(), "1")
    assert result["id"] == "1"


@responses.activate
def test_create_workflow():
    responses.post(f"{API}/workflows", json={"id": "2", "name": "New WF"})
    result = workflows.create_workflow(_client(), "New WF", [], {})
    assert result["id"] == "2"


@responses.activate
def test_create_workflow_with_options():
    responses.post(f"{API}/workflows", json={"id": "3", "name": "Custom WF"})
    result = workflows.create_workflow(
        _client(), "Custom WF", [{"type": "n8n-nodes-base.start"}], {},
        settings={"executionOrder": "v1"}, static_data={"key": "val"},
    )
    assert result["id"] == "3"


@responses.activate
def test_update_workflow():
    responses.put(f"{API}/workflows/1", json={"id": "1", "name": "Updated"})
    result = workflows.update_workflow(_client(), "1", name="Updated")
    assert result["name"] == "Updated"


@responses.activate
def test_delete_workflow():
    responses.delete(f"{API}/workflows/1", json={})
    result = workflows.delete_workflow(_client(), "1")
    assert result["status"] == "deleted"


@responses.activate
def test_activate_workflow():
    responses.post(f"{API}/workflows/1/activate", json={})
    result = workflows.activate_workflow(_client(), "1")
    assert result["active"] is True


@responses.activate
def test_deactivate_workflow():
    responses.post(f"{API}/workflows/1/deactivate", json={})
    result = workflows.deactivate_workflow(_client(), "1")
    assert result["active"] is False


@responses.activate
def test_execute_workflow():
    responses.post(f"{API}/workflows/1/run", json={"data": {"output": "done"}})
    result = workflows.execute_workflow(_client(), "1")
    assert result["data"]["output"] == "done"


@responses.activate
def test_execute_workflow_with_data():
    responses.post(f"{API}/workflows/1/run", json={"data": {"result": "ok"}})
    result = workflows.execute_workflow(_client(), "1", data={"input": "hello"})
    assert "data" in result


@responses.activate
def test_list_active_workflows():
    responses.get(f"{API}/active-workflows", json=["1", "3", "5"])
    result = workflows.list_active_workflows(_client())
    assert len(result) == 3


@responses.activate
def test_get_activation_error():
    responses.get(f"{API}/active-workflows/error/1", json={"message": "Connection failed"})
    result = workflows.get_activation_error(_client(), "1")
    assert result["message"] == "Connection failed"


# =============================================================================
# Execution operations
# =============================================================================


@responses.activate
def test_list_executions():
    responses.get(f"{API}/executions", json={
        "data": [
            {"id": "ex1", "workflowId": "1", "status": "success", "mode": "manual", "startedAt": "2025-01-01", "stoppedAt": "2025-01-01", "finished": True}
        ],
        "nextCursor": None,
    })
    result = executions.list_executions(_client())
    assert len(result["executions"]) == 1
    assert result["executions"][0]["status"] == "success"


@responses.activate
def test_get_execution():
    responses.get(f"{API}/executions/ex1", json={"id": "ex1", "status": "success"})
    result = executions.get_execution(_client(), "ex1")
    assert result["id"] == "ex1"


@responses.activate
def test_delete_execution():
    responses.delete(f"{API}/executions/ex1", json={})
    result = executions.delete_execution(_client(), "ex1")
    assert result["status"] == "deleted"


@responses.activate
def test_retry_execution():
    responses.post(f"{API}/executions/ex1/retry", json={"id": "ex2", "status": "running"})
    result = executions.retry_execution(_client(), "ex1")
    assert result["id"] == "ex2"


@responses.activate
def test_stop_execution():
    responses.post(f"{API}/executions/ex1/stop", json={})
    result = executions.stop_execution(_client(), "ex1")
    assert result["message"] == "Execution stopped"


# =============================================================================
# Credential operations
# =============================================================================


@responses.activate
def test_list_credentials():
    responses.get(f"{API}/credentials", json={
        "data": [
            {"id": "c1", "name": "Slack", "type": "slackApi", "createdAt": "2025-01-01", "updatedAt": "2025-01-02"}
        ],
    })
    result = credentials.list_credentials(_client())
    assert len(result["credentials"]) == 1
    assert result["credentials"][0]["type"] == "slackApi"


@responses.activate
def test_get_credential_schema():
    responses.get(f"{API}/credentials/schema/slackApi", json={"properties": {"token": {"type": "string"}}})
    result = credentials.get_credential_schema(_client(), "slackApi")
    assert "properties" in result


@responses.activate
def test_create_credential():
    responses.post(f"{API}/credentials", json={"id": "c2", "name": "GitHub"})
    result = credentials.create_credential(_client(), "GitHub", "githubApi", {"token": "xxx"})
    assert result["id"] == "c2"


@responses.activate
def test_delete_credential():
    responses.delete(f"{API}/credentials/c1", json={})
    result = credentials.delete_credential(_client(), "c1")
    assert result["status"] == "deleted"


# =============================================================================
# Tag operations
# =============================================================================


@responses.activate
def test_list_tags():
    responses.get(f"{API}/tags", json={
        "data": [
            {"id": "t1", "name": "production", "createdAt": "2025-01-01", "updatedAt": "2025-01-01"}
        ],
    })
    result = tags.list_tags(_client())
    assert len(result["tags"]) == 1
    assert result["tags"][0]["name"] == "production"


@responses.activate
def test_create_tag():
    responses.post(f"{API}/tags", json={"id": "t2", "name": "staging"})
    result = tags.create_tag(_client(), "staging")
    assert result["name"] == "staging"


@responses.activate
def test_delete_tag():
    responses.delete(f"{API}/tags/t1", json={})
    result = tags.delete_tag(_client(), "t1")
    assert result["status"] == "deleted"


# =============================================================================
# Misc operations
# =============================================================================


@responses.activate
def test_list_users():
    responses.get(f"{API}/users", json={
        "data": [
            {"id": "u1", "email": "admin@example.com", "firstName": "Admin", "lastName": "User", "role": "owner", "createdAt": "2025-01-01"}
        ],
    })
    result = misc.list_users(_client())
    assert len(result["users"]) == 1
    assert result["users"][0]["role"] == "owner"


@responses.activate
def test_trigger_webhook():
    responses.post(f"{BASE}/webhook/my-hook", json={"received": True})
    result = misc.trigger_webhook(_client(), "my-hook")
    assert result["received"] is True


@responses.activate
def test_status_connected():
    responses.get(f"{API}/workflows", json={"data": []})
    responses.get(f"{API}/active-workflows", json=["1", "2"])
    result = misc.status(_client())
    assert result["status"] == "connected"
    assert result["active_workflows"] == 2


@responses.activate
def test_status_error():
    responses.get(f"{API}/workflows", body=ConnectionError("refused"))
    result = misc.status(_client())
    assert result["status"] == "error"
