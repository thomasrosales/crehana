import copy
import logging

from sqlalchemy import update
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
            data = self.process_data(result)
            self.post_sync()
        except Exception as exp:
            logger.error(str(exp))
        else:
            return data

    def post_sync(self, *args, **kwargs):
        raise NotImplementedError

    def process_data(self, *args, **kwargs):
        raise NotImplementedError


class IntegrationAPI(Integration):
    def pre_sync(self, *args, **kwargs):
        logger.info(f"Retrieving data from provider: {self.provider}")

    def post_sync(self, *args, **kwargs):
        logger.info("Finishing process")

    def process_data(self, data, *args, **kwargs):
        posts_created, posts_updated = self._create_or_update_posts(data)
        posts = copy.deepcopy(posts_created)
        posts.extend(posts_updated)
        comments_created, comments_updated = self._create_or_update_comments(
            data, posts
        )
        return {
            "posts_created": len(posts_created),
            "posts_updated": len(posts_updated),
            "comments_created": len(comments_created),
            "comments_updated": len(comments_updated),
        }

    def _convert_post_in_dict(self, posts):
        return {post.external_post_id: post.id for post in posts}

    def _create_or_update_comments(self, data, posts):
        db_comments = []
        db_comments_updated = []
        posts = self._convert_post_in_dict(posts)
        for comment in data.comments:
            if (
                comment_db := self.db.query(models.Comment)
                .filter(models.Comment.external_comment_id == comment.id)
                .first()
            ):
                self.db.execute(
                    update(models.Comment)
                    .where(models.Comment.external_comment_id == comment_db.id)
                    .values(
                        name=comment_db.name,
                        email=comment_db.email,
                        body=comment_db.body,
                        post_id=posts[comment.postId],
                    )
                )
                db_comments_updated.append(comment_db)
            else:
                db_comments.append(
                    models.Comment(
                        external_comment_id=comment.id,
                        name=comment.name,
                        email=comment.email,
                        body=comment.body,
                        post_id=posts[comment.postId],
                    )
                )
        if db_comments:
            self.db.bulk_save_objects(db_comments)
            self.db.commit()

        return db_comments, db_comments_updated

    def _create_or_update_posts(self, data):

        db_posts = []
        db_posts_updated = []
        for post in data.posts:
            if (
                post_db := self.db.query(models.Post)
                .filter(models.Post.external_post_id == post.id)
                .first()
            ):
                self.db.execute(
                    update(models.Post)
                    .where(models.Post.external_post_id == post_db.id)
                    .values(
                        user_id=post_db.user_id,
                        title=post_db.title,
                        body=post_db.body,
                    )
                )
                db_posts_updated.append(post_db)

            else:
                db_posts.append(
                    models.Post(
                        external_post_id=post.id,
                        user_id=post.userId,
                        title=post.title,
                        body=post.body,
                    )
                )
        if db_posts:
            self.db.bulk_save_objects(db_posts)
            self.db.commit()

        return db_posts, db_posts_updated
