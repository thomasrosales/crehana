from typing import List, Optional, Union

import strawberry

from src.db import crud
from src.db.database import get_db
from src.db.schemas import Comment, Post, PostCreate

# Strawberry - GraphQL


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
    def list_posts(
        self, skip: Optional[int] = 0, limit: Optional[int] = 100
    ) -> List[PostType]:
        return [
            Post.from_orm(post)
            for post in crud.get_posts(db=next(get_db()), skip=skip, limit=limit)
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_post(self, title: str, body: str) -> PostType:
        post = crud.create_post(
            db=next(get_db()), post=PostCreate(title=title, body=body, user_id=1)
        )
        return Post.from_orm(post)


schema = strawberry.Schema(query=Query, mutation=Mutation)
