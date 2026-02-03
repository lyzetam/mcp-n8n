"""n8n API client with sync requests."""

from __future__ import annotations

import requests

from mcp_n8n.config import get_settings


class N8nClient:
    """Manages requests sessions for n8n API.

    Configuration is loaded from environment variables (N8N_* prefix)
    or a .env file via Pydantic Settings. Explicit constructor params
    override settings values.
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        settings = get_settings()
        self.base_url = (base_url or settings.resolved_base_url).strip().rstrip("/")
        self.api_key = (api_key or settings.api_key).strip()

    @property
    def api_url(self) -> str:
        return f"{self.base_url}/api/v1"

    def _headers(self) -> dict[str, str]:
        return {
            "X-N8N-API-KEY": self.api_key,
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def get(self, endpoint: str, params: dict | None = None) -> dict | list:
        """Synchronous GET request."""
        response = requests.get(
            f"{self.api_url}{endpoint}",
            headers=self._headers(),
            params=params,
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}

    def post(self, endpoint: str, json: dict | None = None) -> dict:
        """Synchronous POST request."""
        response = requests.post(
            f"{self.api_url}{endpoint}",
            headers=self._headers(),
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}

    def put(self, endpoint: str, json: dict | None = None) -> dict:
        """Synchronous PUT request."""
        response = requests.put(
            f"{self.api_url}{endpoint}",
            headers=self._headers(),
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}

    def patch(self, endpoint: str, json: dict | None = None) -> dict:
        """Synchronous PATCH request."""
        response = requests.patch(
            f"{self.api_url}{endpoint}",
            headers=self._headers(),
            json=json,
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}

    def delete(self, endpoint: str) -> dict:
        """Synchronous DELETE request."""
        response = requests.delete(
            f"{self.api_url}{endpoint}",
            headers=self._headers(),
            timeout=30,
        )
        response.raise_for_status()
        return response.json() if response.text else {"status": "success"}

    def webhook(self, path: str, method: str = "POST", json: dict | None = None, params: dict | None = None) -> dict:
        """Send a request to a webhook endpoint (not through /api/v1)."""
        url = f"{self.base_url}/webhook/{path}"
        func = getattr(requests, method.lower())
        kwargs: dict = {"timeout": 30}
        if json:
            kwargs["json"] = json
        if params:
            kwargs["params"] = params

        response = func(url, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"response": response.text}
