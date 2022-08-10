from src.db.schemas import PostType


def get_posts():
    return [
        PostType(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
        ),
    ]
