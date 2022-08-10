from sqlalchemy import ForeignKey, Integer, String, Text, Column
from sqlalchemy.orm import relationship

from src.db.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    title = Column(String(100))
    body = Column(Text)

    # Relationships

    comments = relationship("Comment", back_populates="post")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    email = Column(String, index=True)
    body = Column(Text)

    # Relationships

    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", back_populates="comments")