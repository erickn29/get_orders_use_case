from unittest.mock import patch

from django.test import TestCase

from filemanager.services.dbf_file import DBFFileV2
from order.repository.order import UfarmaOrderRepository
from order.schema.order import OrderSchemaFromFile

import pytest


class TestOrder(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.repository = UfarmaOrderRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    @patch("os.path.exists")
    @patch.object(DBFFileV2, "read_order_ufarma_v2")
    def test_read_order_from_local_file_valid_schema(
        self, mock_read_order, mock_exists
    ):
        mock_exists.return_value = True
        return_data = [
            {
                "numz": "123",
                "date": "2020-01-01",
                "datez": "2020-01-01",
                "code": "123",
                "name": "Name",
                "qtty": 7.0,
                "podrcd": "123",
                "price": 123.0,
                "podr": "podr",
                "md": "123",
            },
            {
                "numz": "123",
                "date": "2020-01-01",
                "datez": "2020-01-01",
                "code": "123",
                "name": "Name2",
                "qtty": 8.0,
                "podrcd": "123",
                "price": 123.0,
                "podr": "podr",
                "md": "123",
            },
        ]
        mock_read_order.return_value = return_data
        result = self.repository.read_order_from_local_file("some/path/file.dbf")
        assert isinstance(result, list)
        assert len(result) == 2
        schema_1 = result[0]
        schema_2 = result[1]
        assert isinstance(schema_1, OrderSchemaFromFile)
        assert isinstance(schema_2, OrderSchemaFromFile)

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    def test_read_order_from_local_file_wrong_path(self):
        result = self.repository.read_order_from_local_file("some/path/file.dbf")
        assert result is None

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    @patch("os.path.exists")
    @patch.object(DBFFileV2, "read_order_ufarma_v2")
    def test_read_order_from_local_file_bad_schema(self, mock_read_order, mock_exists):
        mock_exists.return_value = True
        return_data = [
            {
                "numz": "10101010101",
                "date": "2020-01-01",
                "datez": "2020-01-01",
                "code": "123",
                "name": "Name",
                "qtty": 7.0,
                "podrcd": "123",
                "price": 123.0,
                "podr": "podr",
                "md": "123",
            },
            {
                "numz": "123",
                "date": "2020-01-01",
                "datez": "2020-01-01",
                "code": "123",
                "name": "Name2",
                "qtty": 8.0,
                "podrcd": "123",
                "price": 123.0,
                "podr": "podr",
                "md": "123",
            },
        ]
        mock_read_order.return_value = return_data
        result = self.repository.read_order_from_local_file("some/path/file.dbf")
        assert result is None
