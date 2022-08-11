from typing import List, Union

import strawberry
from pydantic import BaseModel, constr

from src.db import crud
from src.db.database import get_db


class CommentBase(BaseModel):
    post_id: int
    name: constr(max_length=100)
    email: str
    body: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    user_id: int
    title: constr(max_length=100)
    body: str


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True


# Graphene


@strawberry.experimental.pydantic.type(model=Comment, all_fields=True)
class CommentType:
    pass


@strawberry.experimental.pydantic.type(model=Post, all_fields=True)
class PostType:
    pass


@strawberry.type
class Query:
    @strawberry.field
    def get_post(self, post_id: strawberry.ID) -> Union[PostType, None]:
        post = crud.get_post(db=next(get_db()), post_id=post_id)
        return Post.from_orm(post) if post else PostType()

    @strawberry.field
    def list_posts(self) -> List[PostType]:
        return [Post.from_orm(post) for post in crud.get_posts(db=next(get_db()))]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_post(self, title: str, body: str) -> PostType:
        post = crud.create_post(
            db=next(get_db()), post=PostCreate(title=title, body=body, user_id=1)
        )
        return Post.from_orm(post)


schema = strawberry.Schema(query=Query, mutation=Mutation)
