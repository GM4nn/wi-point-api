# strawberry
from strawberry.fastapi import GraphQLRouter
from strawberry import Schema

# resolvers
from app.src.graphql.resolvers.wifi_point_query import WifiPointQuery

# extensions
from app.src.graphql.extensions import SQLAlchemySessionExtension

schema: Schema = Schema(
    query=WifiPointQuery,
    extensions=[SQLAlchemySessionExtension]
)

# if need multiple Queries use this
# all_queries = strawberry.merge_types("ALlQueries", (WifiPointQuery, ..., ...))
# schema = strawberry.Schema(query=Query, extensions=[SQLAlchemySessionExtension])

graphql_router: GraphQLRouter = GraphQLRouter(schema)
