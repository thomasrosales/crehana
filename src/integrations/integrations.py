import logging

from sqlalchemy.orm import Session

from src.db import models

logger = logging.getLogger(__name__)


class Integration:
    provider = None
    db = None

    def __init__(self, db: Session, provider, *args, **kwargs):
        self.db = db
        self.provider = provider

    def pre_sync(self, *args, **kwargs):
        raise NotImplementedError

    def sync(self, *args, **kwargs):
        try:
            self.pre_sync()
            result = self.provider.retrieve_data()
            self.process_data(result)
            self.post_sync()
        except Exception as exp:
            logger.error(str(exp))

    def post_sync(self, *args, **kwargs):
        raise NotImplementedError

    def process_data(self, *args, **kwargs):
        raise NotImplementedError


class IntegrationAPI(Integration):
    def __init__(self, *args, **kwargs):
        super(IntegrationAPI, self).__init__(*args, **kwargs)

    def pre_sync(self, *args, **kwargs):
        pass

    def post_sync(self, *args, **kwargs):
        pass

    def process_data(self, data, *args, **kwargs):
        db_posts = [
            models.Post(
                user_id=post.userId,
                title=post.title,
                body=post.body,
            )
            for post in data.posts
            if not self.db.query(models.Post)
            .filter(
                models.Post.id == post.id,
                models.Post.user_id == post.userId,
                models.Post.title == post.title,
            )
            .first()
        ]

        self.db.bulk_save_objects(db_posts)
        self.db.commit()

        db_comments = [
            models.Comment(
                name=comment.name,
                email=comment.email,
                body=comment.body,
                post_id=comment.postId,
            )
            for comment in data.comments
            if not self.db.query(models.Comment)
            .filter(
                models.Comment.id == comment.id,
                models.Comment.email == comment.email,
                models.Comment.name == comment.name,
            )
            .first()
        ]

        self.db.bulk_save_objects(db_comments)
        self.db.commit()
