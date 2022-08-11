import json

from addict import Dict
from requests import Request, Session

from src.db import crud, models
from src.db.database import get_db
from src.db.schemas import Post, PostCreate


class ProviderException(Exception):
    pass


class Provider:

    db = None
    url = None
    headers = {
        "Content-type": "application/json",
    }

    def __init__(self, url, headers=None, *args, **kwargs):
        if headers is None:
            headers = {}
        self.url = url
        self.headers.update(headers)
        self.db = next(get_db())

    def retrieve_data(self, *args, **kwargs):
        raise NotImplementedError

    def insert_model(self, *args, **kwargs):
        raise NotImplementedError

    def update_model(self, *args, **kwargs):
        raise NotImplementedError

    def partial_update_model(self, *args, **kwargs):
        raise NotImplementedError

    def delete_model(self, *args, **kwargs):
        raise NotImplementedError

    def _requests(self, sub_domain, method, data=None, headers=None):
        s = Session()

        req = Request(method, f"{self.url}/{sub_domain}/", headers=headers)
        if method in ["POST", "PATCH", "PUT"]:
            req = Request(
                method,
                f"{self.url}/{sub_domain}/",
                data=json.dumps(data),
                headers=headers,
            )
        prepped = req.prepare()
        return s.send(prepped)


class JSONPlaceHolderProvider(Provider):
    def __init__(self, *args, **kwargs):
        url = "https://jsonplaceholder.typicode.com"
        super(JSONPlaceHolderProvider, self).__init__(url, *args, **kwargs)

    def _retrieve_posts(self):
        response = self._requests(
            method="GET",
            sub_domain="posts",
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        return Dict({"data": response.json()})

    def _retrieve_comments(self, post_id=None):
        response = self._requests(
            method="GET",
            sub_domain=f"comments?postId={post_id}" if post_id else "comments",
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        return Dict({"data": response.json()})

    def get_models(self):
        """Retrieve all Posts."""
        return self._retrieve_posts()

    def get_model_by_id(self, post_id, with_comments=False):
        """Retrieve Post by Identifier with/without comments."""

        response = self._requests(
            method="GET",
            sub_domain=f"posts/{post_id}/comments"
            if with_comments
            else f"posts/{post_id}",
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        return Dict({"data": response.json()})

    def get_model_and_comments(self, post_id):
        return self.get_model_by_id(post_id, with_comments=True)

    def retrieve_data(self):
        """Retrieving neither posts and comments."""

        posts = self._retrieve_posts()
        comments = self._retrieve_comments()

        return Dict({"posts": posts.data, "comments": comments.data})

    def partial_update_model(self, post, payload):
        """
        Partial update Post resource.

        Example:
        partial_update_model(
            post=Post(id=1, title="test", body="test", user_id=1),
            payload={"title": "hola"},
        )
        """

        if not any(True for key in payload if key in ["title", "body", "user_id"]):
            raise ProviderException("Payload invalid.")

        for key in payload:
            if key not in ["title", "body", "user_id"]:
                del payload[key]

        if payload.get("user_id"):
            user_id = payload["user_id"]
            del payload["user_id"]
            payload["userId"] = user_id

        response = self._requests(
            method="PATCH",
            sub_domain=f"posts/{post.id}",
            data=payload,
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        model_json = Dict(response.json())
        crud.update_post(self.db, post, model_json)
        return Dict({"data": model_json})

    def update_model(self, post: Post, title, body, user_id):
        """
        Update a Post resource.

        Example:

        update_model(
            post=Post(id=1, title="test", body="test", user_id=1),
            title="hola",
            body="hola",
            user_id=1
        )
        """

        payload = {
            "title": title,
            "body": body,
            "userId": user_id,
        }

        response = self._requests(
            method="PUT",
            sub_domain=f"posts/{post.id}",
            data=payload,
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        model_json = Dict(response.json())
        crud.update_post(self.db, post, model_json)
        return Dict({"data": model_json})

    def insert_model(self, title, body, user_id):
        """Create a Post resource."""

        payload = {
            "title": title,
            "body": body,
            "userId": user_id,
        }

        response = self._requests(
            method="POST",
            sub_domain="posts",
            data=payload,
            headers=self.headers,
        )

        if response.status_code != 201:
            raise ProviderException(response.json())

        model_json = Dict(response.json())
        crud.create_post(self.db, PostCreate(**model_json, user_id=model_json.userId))
        return Dict({"data": model_json})

    def delete_model(self, post_id):

        post = self.db.query(models.Post).filter(models.Post.id == post_id).first()

        if not post:
            raise ProviderException("Post does not exists")

        response = self._requests(
            method="DELETE",
            sub_domain=f"posts/{post.external_post_id}",
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        crud.delete_post(self.db, post_id)
