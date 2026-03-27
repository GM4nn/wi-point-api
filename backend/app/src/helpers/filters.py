# typing
from typing import Any

# sqlalchemy
from sqlalchemy import ColumnElement, func

# models
from app.src.models import WifiPoint

# schemas
from app.src.schemas.pagination_params_graphql import PaginationParamsGraphQL



class WifiPointHelper:

    # use the pagination params to extract the filter fields
    def __init__(self, filters: PaginationParamsGraphQL) -> None:
        self._filters: PaginationParamsGraphQL = filters
        self._ref_point: Any = func.ST_GeogFromText(f"POINT({filters.ltg} {filters.lat})")

    def build_proximity_order(self) -> ColumnElement:
        distance: ColumnElement = func.ST_Distance(WifiPoint.location, self._ref_point)
        return distance

    def build_town_all_filter(self) -> ColumnElement[bool]:
        return WifiPoint.town_hall.ilike(
            f"%{self._filters.town_hall.strip()}%"
        )

    def build_filters_and_order(self) -> tuple[list[ColumnElement[bool]], ColumnElement | None]:

        filters: list[ColumnElement[bool]] = []
        order_by: ColumnElement | None = None

        if self._filters.lat and self._filters.ltg:
            order_by = self.build_proximity_order()

        if self._filters.town_hall:
            filters.append(self.build_town_all_filter())

        return filters, order_by