from unittest import TestCase
from unittest.mock import MagicMock, PropertyMock, patch

from src.integrations.integrations import IntegrationAPI
from src.integrations.providers import JSONPlaceHolderProvider


class IntegrationAPITestClass(TestCase):
    def test_sync(self):
        provider_mock = MagicMock()
        db_mock = MagicMock()
        provider_mock.retrieve_data.return_value = {"foo": "bar"}

        integration = IntegrationAPI(db=db_mock, provider=provider_mock)
        with patch(
            "src.integrations.integrations.IntegrationAPI.process_data"
        ) as mock_process_data:
            mock_process_data.return_value = {"foo": "bar"}

            response = integration.sync()

            db_mock.assert_not_called()
            provider_mock.retrieve_data.assert_called_once()
            mock_process_data.assert_called_once()

            assert response == {"foo": "bar"}
