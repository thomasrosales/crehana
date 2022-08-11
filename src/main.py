import logging

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from strawberry.asgi import GraphQL

from src.db import models
from src.db.database import engine, get_db
from src.db.schemas import schema
from src.integrations.integrations import IntegrationAPI
from src.integrations.providers import JSONPlaceHolderProvider

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

graphql_app = GraphQL(schema)

app = FastAPI()


app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get(
    "/call_integration/",
)
def call_integration(
    db: Session = Depends(get_db),
):
    provider = JSONPlaceHolderProvider()
    integration = IntegrationAPI(db=db, provider=provider)
    data = integration.sync()
    return {
        "Integration Sync": "Finished",
        "data": data,
    }
