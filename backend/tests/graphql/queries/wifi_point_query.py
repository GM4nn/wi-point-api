from graphql_query import Query, Field, Argument


WIFI_POINT_QUERY_NOT_FOUND = Query(
    name="wifiPoint",
    arguments=[
        Argument(
            name="originalId",
            value='"without id"'
        )
    ],
    fields=[
        Field(name="id"),
        Field(name="originalId"),
        Field(name="programa"),
        Field(name="alcaldia"),
        Field(name="latitud"),
        Field(name="longitud"),
    ],
).render()

WIFI_POINT_QUERY = Query(
    name="wifiPoint",
    arguments=[
        Argument(
            name="originalId",
            value='"MEX-AIM-AER-AICMT1-M-GW001"'
        )
    ],
    fields=[
        Field(name="id"),
        Field(name="originalId"),
        Field(name="programa"),
        Field(name="alcaldia"),
        Field(name="latitud"),
        Field(name="longitud"),
    ],
).render()
