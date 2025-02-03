from django.test import TestCase

from order.factories import DistributorFactory, OrderFactory
from order.repository.order import UfarmaOrderRepository

import pytest


class TestOrder(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.distributor = DistributorFactory(title="ufarma")
        cls.order = OrderFactory(distributor=cls.distributor)
        cls.repository = UfarmaOrderRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    def test_get_or_create_false(self):
        obj, created = self.repository.get_or_create(
            distributor=self.distributor,
            numz=self.order.numz,
            datez=self.order.datez,
            date=self.order.date,
            podr=self.order.podr,
            podrcd=self.order.podrcd,
            md=self.order.md,
            partn=self.order.partn,
            zak_ustr1=self.order.zak_ustr1,
        )
        assert obj.id == self.order.id
        assert created is False

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    def test_get_or_create_true(self):
        obj, created = self.repository.get_or_create(
            distributor=self.distributor,
            numz=self.order.numz + "1",
            datez=self.order.datez,
            date=self.order.date,
            podr=self.order.podr,
            podrcd=self.order.podrcd,
            md=self.order.md,
            partn=self.order.partn,
            zak_ustr1=self.order.zak_ustr1,
        )
        assert created is True
        assert obj.id != self.order.id
