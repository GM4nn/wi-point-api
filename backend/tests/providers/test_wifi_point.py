
# Mock
from unittest.mock import MagicMock

# provider
from app.src.providers.wifi_point import WifiPointProvider

# graphql classes
from app.src.schemas.paginated_response_graphql import PaginatedResponseGraphQL
from app.src.schemas.wifi_point_graphql import WifiPointGraphQL

# factory to create random data
from tests.factories.wifi_point import WifiPointFactory


class TestWifiPointProvider:

    def test_get_by_original_id_found(
        self,
        mock_db: MagicMock
    ) -> None:

        wifi_original_id_fake: str = "WIFI-0001"
        town_hall: str = "Tlalpan"

        fake_wifi_point: WifiPointFactory = WifiPointFactory(
            original_id=wifi_original_id_fake,
            town_hall=town_hall
        )

        # this mock to simulate return value of filter sqlalchemy
        mock_db.query.return_value.filter.return_value.first.return_value = fake_wifi_point

        provider: WifiPointProvider = WifiPointProvider(mock_db)
        result: WifiPointGraphQL = provider.get_by_original_id(wifi_original_id_fake)

        assert isinstance(result, WifiPointGraphQL)
        assert result.original_id == wifi_original_id_fake
        assert result.alcaldia == town_hall

    def test_get_by_original_id_not_found(
        self,
        mock_db: MagicMock
    ) -> None:

        mock_db.query.return_value.filter.return_value.first.return_value = None

        provider: WifiPointProvider = WifiPointProvider(mock_db)
        result: None = provider.get_by_original_id("NOT EXISTS")

        assert result is None

    def test_get_all_paginated_empty(
        self,
        mock_db: MagicMock
    ) -> None:

        provider: WifiPointProvider = WifiPointProvider(mock_db)
        result: PaginatedResponseGraphQL = provider.get_all_paginated(offset=0, limit=10)

        assert isinstance(result, PaginatedResponseGraphQL)
        assert result.pagination.total_data == 0
        assert result.data == []

    def test_get_all_paginated_with_data(
        self,
        mock_db: MagicMock
    ) -> None:

        fake_points: list[MagicMock] = WifiPointFactory.create_batch(3)

        mock_db.query.return_value.count.return_value = 3
        mock_db.query.return_value.offset.return_value.limit.return_value.all.return_value = fake_points

        provider: WifiPointProvider = WifiPointProvider(mock_db)
        result: PaginatedResponseGraphQL = provider.get_all_paginated(offset=0, limit=10)

        assert isinstance(result, PaginatedResponseGraphQL)
        assert result.pagination.total_data == 3
        assert len(result.data) == 3
        assert result.pagination.current_page == 1
