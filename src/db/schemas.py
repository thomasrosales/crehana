from typing import List

from pydantic import BaseModel, constr


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
