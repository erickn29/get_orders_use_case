from django.test import TestCase

from order.factories import DistributorFactory, PharmacyModelFactory
from order.repository.pharmacy import PharmacyRepository

import pytest


class TestPharmacy(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.distributor = DistributorFactory(title="ufarma")
        cls.pharmacy = PharmacyModelFactory(distributor=cls.distributor)
        cls.repository = PharmacyRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.pharmacy_repository
    def test_find(self):
        pharmacy = self.repository.find(external_code=self.pharmacy.external_code)
        assert pharmacy.id == self.pharmacy.id

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.pharmacy_repository
    def test_find_none(self):
        pharmacy = self.repository.find(external_code="123")
        assert pharmacy is None
