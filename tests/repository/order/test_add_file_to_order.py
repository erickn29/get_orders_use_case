from django.test import TestCase

from filemanager.factories import FileFactory
from order.factories import DistributorFactory, OrderFactory
from order.repository.order import UfarmaOrderRepository

import pytest


class Test(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.distributor = DistributorFactory(title="ufarma")
        cls.order = OrderFactory(distributor=cls.distributor)
        cls.file = FileFactory(author=None)
        cls.repository = UfarmaOrderRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    def test_add_file_to_order(self):
        assert self.order.file is None
        self.repository.add_file_to_order(self.order, self.file)
        assert self.order.file == self.file

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.order_repository
    def test_add_file_to_order_no_file(self):
        assert self.order.file is None
        self.repository.add_file_to_order(self.order, None)
        assert self.order.file is None
