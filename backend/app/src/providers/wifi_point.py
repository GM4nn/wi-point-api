# other lib
from math import ceil

# sqlalchemy
from sqlalchemy import ColumnElement, UnaryExpression
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query

# schemas
from app.src.schemas.paginated_response_graphql import PaginatedResponseGraphQL, PaginationGraphQL
from app.src.schemas.wifi_point_graphql import WifiPointGraphQL

# models
from app.src.models import WifiPoint


class WifiPointProvider:

    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    def get_by_id(self, point_id: int) -> WifiPointGraphQL | None:
        
        wifi_point =  self._db_session.query(WifiPoint).get(point_id)

        if wifi_point:
            return WifiPointGraphQL.from_instance(wifi_point)

    def get_pagination_data(
        self,
        offset: int,
        limit: int,
    ) -> PaginationGraphQL:

        total_data: int = self._db_session.query(WifiPoint.id).count()
        total_pages_or_last_page: int = ceil(total_data / limit ) or 1

        current_page: int = (offset // limit ) + 1
        next_page: int = current_page + 1
        prev_page: int = current_page - 1

        return PaginationGraphQL(
            total_data=total_data,
            total_pages=total_pages_or_last_page,
            current_page=current_page,
            next_page=next_page,
            prev_page=prev_page,
            last_page=total_pages_or_last_page,
        )

    def get_all_paginated(
        self,
        offset: int,
        limit: int,
        filters: list[ColumnElement[bool]] | None = None,
        order_by: UnaryExpression | ColumnElement | None = None,
    ) -> PaginatedResponseGraphQL:

        pagination_data: PaginationGraphQL = self.get_pagination_data(offset, limit)
        query_wifi_point: Query[WifiPoint] = self._db_session.query(WifiPoint)

        if filters:
            for f in filters:
                query_wifi_point = query_wifi_point.filter(f)

        if order_by:
            query_wifi_point = query_wifi_point.order_by(order_by)

        wifi_points: list[WifiPoint] = query_wifi_point\
            .offset(offset)\
            .limit(limit)\
            .all()

        return PaginatedResponseGraphQL(
            pagination=pagination_data,
            data=[WifiPointGraphQL.from_instance(p) for p in wifi_points],
        )



        