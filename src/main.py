import logging
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.db import crud, models, schemas
from src.db.database import SessionLocal, engine
from src.integrations.integrations import IntegrationAPI
from src.integrations.providers import JSONPlaceHolderProvider

logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    integration.sync()
    return {"Integration Sync": "Finished"}


@app.get(
    "/posts/",
    response_model=List[schemas.Post],
)
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_posts(db, skip=skip, limit=limit)


@app.get(
    "/posts/{post_id}/",
    response_model=schemas.Post,
)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="POst not found")
    return db_post


@app.get(
    "/comments/",
    response_model=List[schemas.Comment],
)
def read_comments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_comments(db, skip=skip, limit=limit)
