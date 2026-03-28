# Server test
from fastapi.testclient import TestClient
from requests import Response

# wifi points queries
from tests.graphql.queries.wifi_points_query import WIFI_POINTS_QUERY_WITH_COORDINATES, WIFI_POINTS_QUERY_WITH_TOWN_HALL
from tests.graphql.queries.wifi_point_query import WIFI_POINT_QUERY, WIFI_POINT_QUERY_NOT_FOUND

# function gql to structure of query
from tests.conftest import gql


class TestWifiPointsEndpoint:

    def test_graphql_endpoint_exists(
        self,
        client: TestClient
    ) -> None:
        response: Response = client.post(
            "/graphql",
            json={
                "query": "{ __typename }"
            }
        )
        assert response.status_code == 200

    def test_wifi_points_simple(
        self,
        client: TestClient
    ) -> None:
        response: Response = client.post(
            "/graphql",
            json=gql(WIFI_POINT_QUERY)
        )
        assert response.status_code == 200

        body: dict = response.json()
        assert "data" in body

    def test_wifi_points_with_coordinates(
        self,
        client: TestClient
    ) -> None:
        response: Response = client.post(
            "/graphql",
            json=gql(WIFI_POINTS_QUERY_WITH_COORDINATES)
        )
        assert response.status_code == 200

        body: dict = response.json()
        assert "data" in body

    def test_wifi_point_with_town_hall(
        self,
        client: TestClient
    ) -> None:
        response: Response = client.post(
            "/graphql",
            json=gql(WIFI_POINTS_QUERY_WITH_TOWN_HALL)
        )
        assert response.status_code == 200

        body: dict = response.json()
        assert "data" in body

    def test_wifi_point_not_found(
        self,
        client: TestClient
    ) -> None:
        response: Response = client.post(
            "/graphql",
            json=gql(WIFI_POINT_QUERY_NOT_FOUND)
        )
        assert response.status_code == 200

        body: dict = response.json()
        assert body["data"]["wifiPoint"] is None
