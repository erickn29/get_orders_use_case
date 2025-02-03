from django.test import TestCase

from order.factories import DistributorFactory, OrderFactory, OrderItemFactory
from order.repository.order_item import OrderItemRepository

import pytest


class TestOrderItem(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.distributor = DistributorFactory(title="ufarma")
        cls.order = OrderFactory(distributor=cls.distributor)
        cls.order_item = OrderItemFactory(order=cls.order)
        cls.repository = OrderItemRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_item_repository
    def test_get_or_create_false(self):
        obj, created = self.repository.get_or_create(
            order=self.order,
            code=self.order_item.code,
            ean13=self.order_item.ean13,
        )
        assert obj.id == self.order_item.id
        assert created is False

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_item_repository
    def test_get_or_create_true(self):
        obj, created = self.repository.get_or_create(
            order=self.order,
            code=self.order_item.code + "1",
            ean13=self.order_item.ean13,
        )
        assert created is True
        assert obj.id != self.order_item.id
