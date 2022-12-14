"""adding external id column to posts and comments models

Revision ID: 9338a9bec1e1
Revises: ff0610ae2eb2
Create Date: 2022-08-11 09:16:27.194875

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9338a9bec1e1"
down_revision = "ff0610ae2eb2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "comments", sa.Column("external_comment_id", sa.Integer(), nullable=True)
    )
    op.create_index(
        op.f("ix_comments_external_comment_id"),
        "comments",
        ["external_comment_id"],
        unique=False,
    )
    op.add_column("posts", sa.Column("external_post_id", sa.Integer(), nullable=True))
    op.create_index(
        op.f("ix_posts_external_post_id"), "posts", ["external_post_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_posts_external_post_id"), table_name="posts")
    op.drop_column("posts", "external_post_id")
    op.drop_index(op.f("ix_comments_external_comment_id"), table_name="comments")
    op.drop_column("comments", "external_comment_id")
    # ### end Alembic commands ###
