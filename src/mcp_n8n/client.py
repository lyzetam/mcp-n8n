"""n8n API client with sync requests."""

from __future__ import annotations

import os

import requests


class N8nClient:
    """Manages requests sessions for n8n API.

    Reads configuration from environment variables:
    - N8N_BASE_URL (default: http://localhost:5678)
    - N8N_API_KEY
    """

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        raw_host = os.environ.get("N8N_HOST", "localhost:5678").strip()
        raw_protocol = os.environ.get("N8N_PROTOCOL", "http").strip()
        default_url = f"{raw_protocol}://{raw_host}"

        self.base_url = (base_url or os.environ.get("N8N_BASE_URL", default_url)).strip().rstrip("/")
        self.api_key = (api_key or os.environ.get("N8N_API_KEY", "")).strip()

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
