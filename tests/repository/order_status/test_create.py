from django.test import TestCase

from order.factories import DistributorFactory, OrderFactory
from order.models import OrderStatus
from order.repository.order_status import OrderStatusRepository

import pytest


class TestOrderStatus(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.distributor = DistributorFactory(title="ufarma")
        cls.order = OrderFactory(distributor=cls.distributor)
        cls.repository = OrderStatusRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_status_repository
    def test_create(self):
        statuses = self.repository.get_all()
        assert len(statuses) == 0
        self.repository.create(
            order=self.order,
            status=OrderStatus.Status.NEW,
        )
        statuses = self.repository.get_all()
        assert len(statuses) == 1
