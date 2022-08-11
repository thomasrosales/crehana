from unittest.mock import patch

from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_call_integration():
    with patch("src.integrations.integrations.Integration.sync") as mock_sync:
        mock_sync.return_value = data = {
            "posts_created": 100,
            "posts_updated": 0,
            "comments_created": 500,
            "comments_updated": 0,
        }
        expected = {
            "Integration Sync": "Finished",
            "data": data,
        }
        response = client.get("/call_integration/")

        assert response.status_code == 200
        assert response.json() == expected
