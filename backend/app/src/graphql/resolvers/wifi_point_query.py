# strawberry
import strawberry

# sqlalchemy
from sqlalchemy import ColumnElement
from sqlalchemy.orm import Session

# schemas
from app.src.schemas.paginated_response_graphql import PaginatedResponseGraphQL
from app.src.schemas.pagination_params_graphql import PaginationParamsGraphQL
from app.src.schemas.wifi_point_graphql import WifiPointGraphQL

# helpers
from app.src.helpers.filters import WifiPointHelper

# providers
from app.src.providers.wifi_point import WifiPointProvider


@strawberry.type
class WifiPointQuery:

    @strawberry.field(description="Lista paginada de todos los puntos WiFi")
    def wifi_points(
        self,
        info: strawberry.types.Info,
        params: PaginationParamsGraphQL
    ) -> PaginatedResponseGraphQL:

        db: Session = info.context["db"]

        provider: WifiPointProvider = WifiPointProvider(db)
        helper: WifiPointHelper = WifiPointHelper(params)

        filters: list[ColumnElement[bool]] = []
        order_by: ColumnElement | None = None
        filters, order_by = helper.build_filters_and_order()

        return provider.get_all_paginated(
            offset=params.offset,
            limit=params.limit,
            filters=filters,
            order_by=order_by,
        )

    @strawberry.field(description="Obtener un punto WiFi por su original_id")
    def wifi_point(
        self,
        info: strawberry.types.Info,
        original_id: str = strawberry.argument(description="ID original del punto WiFi")
    ) -> WifiPointGraphQL | None:
        db: Session = info.context["db"]

        provider: WifiPointProvider = WifiPointProvider(db)
        return provider.get_by_original_id(original_id)
