from __future__ import annotations

import strawberry

from app.src.schemas.wifi_point_graphql import WifiPointGraphQL

@strawberry.type
class PaginationGraphQL:
    total_data: int = strawberry.field(description="Total de registros que coinciden")
    total_pages: int = strawberry.field(description="Total de paginas")
    current_page: int = strawberry.field(description="Pagina actual")
    next_page: int = strawberry.field(description="Pagina siguiente")
    prev_page: int = strawberry.field(description="Pagina anterior")
    last_page: int = strawberry.field(description="Ultima pagina")
    first_page: int = strawberry.field(default=1, description="Primera pagina")

    @classmethod
    def from_instance(cls, instance: PaginationGraphQL) -> PaginationGraphQL:
        return cls(
            total_data=instance.total_data,
            total_pages=instance.total_pages,
            current_page=instance.current_page,
            next_page=instance.next_page,
            prev_page=instance.prev_page,
            last_page=instance.last_page,
            first_page=instance.firts_page,
        )


@strawberry.type
class PaginatedResponseGraphQL:
    pagination: PaginationGraphQL
    data: list[WifiPointGraphQL]
