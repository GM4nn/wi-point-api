import strawberry


@strawberry.input
class PaginationParamsGraphQL:
    limit: int = strawberry.field(default=10, description="Limite de datos por pagina")
    offset: int = strawberry.field(default=0, description="Elementos a saltar")
    town_hall: str | None = strawberry.field(default=None, description="Alcaldia")
    lat: float | None = strawberry.field(default=None, description="Latitud")
    ltg: float | None = strawberry.field(default=None, description="Longitud")
