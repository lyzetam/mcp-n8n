"""Tests for LangChain tool interfaces."""

from langchain_core.tools import BaseTool

from mcp_n8n.langchain_tools import TOOLS


def test_tools_count():
    assert len(TOOLS) == 25


def test_all_tools_are_base_tool():
    for t in TOOLS:
        assert isinstance(t, BaseTool), f"{t} is not a BaseTool"


def test_tool_names_follow_convention():
    for t in TOOLS:
        assert t.name.startswith("n8n_"), f"Tool {t.name} does not follow n8n_ naming convention"


def test_tool_names_are_unique():
    names = [t.name for t in TOOLS]
    assert len(names) == len(set(names)), f"Duplicate tool names: {names}"


def test_expected_tools_present():
    names = {t.name for t in TOOLS}
    expected = {
        # Workflows
        "n8n_list_workflows",
        "n8n_get_workflow",
        "n8n_create_workflow",
        "n8n_update_workflow",
        "n8n_delete_workflow",
        "n8n_activate_workflow",
        "n8n_deactivate_workflow",
        "n8n_execute_workflow",
        "n8n_list_active_workflows",
        "n8n_get_activation_error",
        # Executions
        "n8n_list_executions",
        "n8n_get_execution",
        "n8n_delete_execution",
        "n8n_retry_execution",
        "n8n_stop_execution",
        # Credentials
        "n8n_list_credentials",
        "n8n_get_credential_schema",
        "n8n_create_credential",
        "n8n_delete_credential",
        # Tags
        "n8n_list_tags",
        "n8n_create_tag",
        "n8n_delete_tag",
        # Misc
        "n8n_list_users",
        "n8n_trigger_webhook",
        "n8n_status",
    }
    assert expected == names


def test_all_tools_have_descriptions():
    for t in TOOLS:
        assert t.description, f"Tool {t.name} has no description"
