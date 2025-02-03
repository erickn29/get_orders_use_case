from django.test import TestCase

from order.factories import FTPModelFactory
from order.repository.ftp import FTPRepository

import pytest


class TestWithObjects(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ftp_ufarma = FTPModelFactory(protocol="ufarma")
        cls.ftp_smart_apteka = FTPModelFactory(protocol="smart_apteka")
        cls.ftp_eapteka = FTPModelFactory(protocol="eapteka")
        cls.ftp_dimfarm = FTPModelFactory(protocol="dimfarm")

        cls.repository = FTPRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.ftp_repository
    def test_get_all_len_4(self):
        ftp_objects = self.repository.get_all()
        assert len(ftp_objects) == 4
        assert ftp_objects[0].id == self.ftp_ufarma.id
        assert ftp_objects[1].id == self.ftp_smart_apteka.id
        assert ftp_objects[2].id == self.ftp_eapteka.id
        assert ftp_objects[3].id == self.ftp_dimfarm.id


class TestWithoutObjects(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.repository = FTPRepository()

    @pytest.mark.new_tests
    @pytest.mark.repository
    @pytest.mark.ftp_repository
    def test_get_all_len_0(self):
        ftp_objects = self.repository.get_all()
        assert len(ftp_objects) == 0
