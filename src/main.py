import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from src.schema import schema

app = FastAPI(title="GraphQL Example")

@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "message": "GraphQL Example is running.",
        "graphql_url": "/graphql",
    }

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")