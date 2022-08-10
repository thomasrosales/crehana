from addict import Dict
from requests import Request, Session


class ProviderException(Exception):
    pass


class Provider:

    url = None
    headers = {
        "Content-type": "application/json",
    }

    def __init__(self, url, headers=None, *args, **kwargs):
        if headers is None:
            headers = {}
        self.url = url
        self.headers.update(headers)

    def retrieve_data(self, *args, **kwargs):
        raise NotImplementedError

    def insert_to_model(self, model, *args, **kwargs):
        raise NotImplementedError

    def update_to_model(self, model, *args, **kwargs):
        raise NotImplementedError

    def partial_update_to_model(self, model, *args, **kwargs):
        raise NotImplementedError

    def delete_to_model(self, model, *args, **kwargs):
        raise NotImplementedError

    def _requests(self, sub_domain, method, data=None, headers=None):
        sub_domain = sub_domain.replace("/", "")
        s = Session()

        req = Request(method, f"{self.url}/{sub_domain}/", headers=headers)
        if method in ["POST", "PATCH", "PUT"]:
            req = Request(
                method,
                f"{self.url}/{sub_domain}/",
                data=data,
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

    def _retrieve_comments(self):
        response = self._requests(
            method="GET",
            sub_domain="comments",
            headers=self.headers,
        )

        if response.status_code != 200:
            raise ProviderException(response.json())

        return Dict({"data": response.json()})

    def retrieve_data(self, *args, **kwargs):
        posts = self._retrieve_posts()
        comments = self._retrieve_comments()

        return Dict({"posts": posts.data, "comments": comments.data})
