from graphql_query import Query, Field, Argument

data_fields = Field(
    name="data",
    fields=[
        Field(name="alcaldia"),
        Field(name="id"),
        Field(name="latitud"),
        Field(name="longitud"),
        Field(name="originalId"),
        Field(name="programa"),
    ],
)

pagination_fields = Field(
    name="pagination",
    fields=[
        Field(name="currentPage"),
        Field(name="firstPage"),
        Field(name="lastPage"),
        Field(name="nextPage"),
        Field(name="prevPage"),
        Field(name="totalData"),
        Field(name="totalPages"),
    ],
)

WIFI_POINTS_QUERY = Query(
    name="wifiPoints",
    arguments=[
        Argument(
            name="params", 
            value=[
                Argument(
                    name="limit",
                    value=10
                ),
                Argument(
                    name="offset",
                    value=10
                ),
            ]
        ),
    ],
    fields=[
        data_fields,
        pagination_fields
    ],
).render()


WIFI_POINTS_QUERY_WITH_COORDINATES = Query(
    name="wifiPoints",
    arguments=[
        Argument(
            name="params", 
            value=[
                Argument(
                    name="limit",
                    value=10
                ),
                Argument(
                    name="offset",
                    value=10
                ),
                Argument(
                    name="ltg",
                    value=-99.116341
                ),
                Argument(
                    name="lat",
                    value=19.263566
                ),
            ]
        ),
    ],
    fields=[
        data_fields,
        pagination_fields
    ],
).render()


WIFI_POINTS_QUERY_WITH_TOWN_HALL = Query(
    name="wifiPoints",
    arguments=[
        Argument(
            name="params", 
            value=[
                Argument(
                    name="limit",
                    value=10
                ),
                Argument(
                    name="offset",
                    value=10
                ),
                Argument(
                    name="townHall",
                    value='"Iztapalapa"'
                ),
            ]
        ),
    ],
    fields=[
        data_fields,
        pagination_fields
    ],
).render()