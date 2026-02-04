# mcp-n8n

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

n8n workflow automation API as a Python library, LangChain tools, and MCP server. Manage workflows, executions, credentials, tags, users, and webhooks from code or an MCP-compatible client.

## Features

**25 tools** across 5 categories:

- **Workflows** (10) -- list, get, create, update, delete, activate, deactivate, execute, list active, get activation errors
- **Executions** (5) -- list, get, delete, retry, stop
- **Credentials** (4) -- list, get schema, create, delete
- **Tags** (3) -- list, create, delete
- **Misc** (3) -- list users, trigger webhook, check status

## Installation

```bash
# Core library only
pip install .

# With MCP server
pip install ".[mcp]"

# With LangChain tools
pip install ".[langchain]"

# Everything
pip install ".[all]"
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `N8N_API_KEY` | n8n API key | (required) |
| `N8N_HOST` | n8n host and port | `localhost:5678` |
| `N8N_PROTOCOL` | Protocol (http or https) | `http` |
| `N8N_BASE_URL` | Full base URL (overrides protocol + host) | (computed) |

Create a `.env` file:

```env
N8N_API_KEY=your-n8n-api-key
N8N_HOST=localhost:5678
N8N_PROTOCOL=http
```

## Quick Start

### MCP Server

```bash
mcp-n8n
```

### LangChain Tools

```python
from mcp_n8n.langchain_tools import TOOLS, n8n_list_workflows

# Use individual tools
result = n8n_list_workflows.invoke({})

# Or pass all tools to an agent
from langchain.agents import AgentExecutor
agent = AgentExecutor(tools=TOOLS, ...)
```

### Python Library

```python
from mcp_n8n.client import N8nClient

client = N8nClient()
workflows = client.get_sync("/workflows")
```

## License

MIT
