from sqlalchemy import update
from sqlalchemy.orm import Session

from . import models, schemas


def get_post(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def get_post_by_user(db: Session, user_id: int):
    return db.query(models.Post).filter(models.Post.user_id == user_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Post).offset(skip).limit(100).all()


def create_post(db: Session, post: schemas.PostCreate):
    db_post = models.Post(
        user_id=post.user_id,
        title=post.title,
        body=post.body,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post: schemas.PostCreate, data):
    db.execute(
        update(models.Post)
        .where(models.Post.external_post_id == data.id)
        .values(
            user_id=data.userId,
            title=data.title,
            body=data.body,
        )
    )
    return db.query(models.Post).filter(models.Post.external_post_id == data.id).first()


def delete_post(db: Session, post_id: int):
    db.query(models.Comment).filter(models.Comment.post_id == post_id).delete()
    db.query(models.Post).filter(models.Post.id == post_id).delete()
    db.commit()


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Comment).offset(skip).limit(100).all()


def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Comment)
        .filter(models.Post.id == post_id)
        .offset(skip)
        .limit(100)
        .all()
    )


def create_comment(db: Session, comment: schemas.CommentCreate, post_id: int):
    db_comment = models.Comment(
        **comment,
        post_id=post_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
