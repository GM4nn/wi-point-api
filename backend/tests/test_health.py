# server test
from fastapi.testclient import TestClient

# Response type
from requests import Response


class TestHealthCheck:

    def test_returns_ok(
        self,
        client: TestClient
    ) -> None:

        response: Response = client.get("/")
        assert response.status_code == 200

    def test_response_body(
        self,
        client: TestClient
    ) -> None:

        response: Response = client.get("/")
        data: dict = response.json()

        assert data["status"] == "ok"
        assert data["service"] == "wifi-cdmx-api"
