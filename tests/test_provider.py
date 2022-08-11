from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch

from src.db.schemas import Post
from src.integrations.providers import JSONPlaceHolderProvider


class JSONPlaceHolderProviderTestClass(TestCase):
    def setUp(self):
        self.provider = JSONPlaceHolderProvider()

    def _get_response_mock(self, status_code_return=200, json_return=None):
        response_mock = MagicMock()
        status_code = PropertyMock(return_value=status_code_return)
        type(response_mock).status_code = status_code
        response_mock.json.return_value = json_return or {"foo": "bar"}
        return response_mock

    def test_get_models(self):
        with patch("src.integrations.providers.Provider._requests") as mock__requests:
            mock__requests.return_value = self._get_response_mock()

            response = self.provider.get_models()

            assert response.data == {"foo": "bar"}
            mock__requests.assert_called_with(
                method="GET",
                sub_domain="posts",
                headers=self.provider.headers,
            )

    def test_get_model_by_id(self):
        with patch("src.integrations.providers.Provider._requests") as mock__requests:
            mock__requests.return_value = self._get_response_mock()

            response = self.provider.get_model_by_id(10)

            assert response.data == {"foo": "bar"}
            mock__requests.assert_called_with(
                method="GET",
                sub_domain=f"posts/{10}",
                headers=self.provider.headers,
            )

            response = self.provider.get_model_by_id(10, with_comments=True)

            assert response.data == {"foo": "bar"}
            mock__requests.assert_called_with(
                method="GET",
                sub_domain=f"posts/{10}/comments",
                headers=self.provider.headers,
            )

    def test_get_model_and_comments(self):
        with patch("src.integrations.providers.Provider._requests") as mock__requests:
            mock__requests.return_value = self._get_response_mock()

            response = self.provider.get_model_and_comments(10)

            assert response.data == {"foo": "bar"}
            mock__requests.assert_called_with(
                method="GET",
                sub_domain=f"posts/{10}/comments",
                headers=self.provider.headers,
            )

    def test_retrieve_data(self):
        with patch("src.integrations.providers.Provider._requests") as mock__requests:
            mock__requests.return_value = self._get_response_mock()

            response = self.provider.retrieve_data()

            assert response == {
                "posts": {"foo": "bar"},
                "comments": {"foo": "bar"},
            }
            assert mock__requests.call_count == 2

    def test_partial_update_model(self):
        with patch(
            "src.integrations.providers.Provider._requests"
        ) as mock__requests, patch("src.db.crud.update_post") as mock_update_post:
            mock__requests.return_value = self._get_response_mock()
            mock_update_post.return_value = True
            response = self.provider.partial_update_model(
                Post(id=1, title="test", body="test", user_id=1),
                payload={"title": "hola"},
            )

            mock__requests.assert_called_with(
                method="PATCH",
                sub_domain="posts/1",
                data={"title": "hola"},
                headers=self.provider.headers,
            )

            mock_update_post.assert_called()
            assert response.data == {"foo": "bar"}

    def test_update_model(self):
        with patch(
            "src.integrations.providers.Provider._requests"
        ) as mock__requests, patch("src.db.crud.update_post") as mock_update_post:
            mock__requests.return_value = self._get_response_mock()
            mock_update_post.return_value = True
            response = self.provider.update_model(
                post=Post(id=1, title="test", body="test", user_id=1),
                title="hola",
                body="hola",
                user_id=1,
            )

            mock__requests.assert_called_with(
                method="PUT",
                sub_domain="posts/1",
                data={
                    "title": "hola",
                    "body": "hola",
                    "userId": 1,
                },
                headers=self.provider.headers,
            )

            mock_update_post.assert_called()
            assert response.data == {"foo": "bar"}

    def test_insert_model(self):
        with patch(
            "src.integrations.providers.Provider._requests"
        ) as mock__requests, patch(
            "src.db.crud.create_post"
        ) as mock_create_post, patch(
            "src.integrations.providers.PostCreate"
        ):
            mock__requests.return_value = self._get_response_mock(
                status_code_return=201
            )
            mock_create_post.return_value = True

            response = self.provider.insert_model(
                title="hola",
                body="hola",
                user_id=1,
            )

            mock__requests.assert_called_with(
                method="POST",
                sub_domain="posts",
                data={
                    "title": "hola",
                    "body": "hola",
                    "userId": 1,
                },
                headers=self.provider.headers,
            )

            mock_create_post.assert_called()
            assert response.data == {"foo": "bar"}

    def test_delete_model(self):
        with patch(
            "src.integrations.providers.Provider._requests"
        ) as mock__requests, patch("src.db.crud.delete_post") as mock_delete_post:
            mock__requests.return_value = self._get_response_mock()
            mock_delete_post.return_value = True

            self.provider.delete_model(1)

            mock__requests.assert_called_with(
                method="DELETE",
                sub_domain=f"posts/{1}",
                headers=self.provider.headers,
            )
