from datetime import datetime
from unittest.mock import patch

from django.core.cache import cache as CacheService
from django.test import TestCase

from filemanager.services.dbf_file import DBFFileV2
from filemanager.services.xml_file import XMLFile
from order.factories import DistributorFactory, FTPModelFactory, PharmacyModelFactory
from order.models import Order
from order.repository.file import FileRepository
from order.service.file import FileServiceV1
from order.service.ftp.ftp_orm import FTPORMServiceV1
from order.service.ftp.ftp_server import FTPServerV1
from order.service.order_item import OrderItemServiceV1
from order.service.order_status import OrderStatusServiceV1
from order.service.pharmacy import PharmacyServiceV1
from order.use_case.order.get_orders_from_ftp import GetOrdersUseCase
from utils.other import LogServiceV1

from override_storage import override_storage


class TestGetOrders(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ftp_ufarma = FTPModelFactory(protocol="ufarma")
        cls.ftp_smart_apteka = FTPModelFactory(protocol="smart_apteka")
        cls.ftp_eapteka = FTPModelFactory(protocol="eapteka")
        cls.ftp_dimfarm = FTPModelFactory(protocol="dimfarm")

        cls.distributor_ufarma = DistributorFactory(protocol="ufarma")
        cls.distributor_smart_apteka = DistributorFactory(protocol="smart_apteka")
        cls.distributor_eapteka = DistributorFactory(protocol="eapteka")
        cls.distributor_dimfarm = DistributorFactory(protocol="dimfarm")

        cls.pharmacy_ufarma = PharmacyModelFactory(
            distributor=cls.distributor_ufarma,
            external_code="1u",
        )
        cls.pharmacy_smart_apteka = PharmacyModelFactory(
            distributor=cls.distributor_smart_apteka,
            external_code="1s",
        )
        cls.pharmacy_eapteka = PharmacyModelFactory(
            distributor=cls.distributor_eapteka,
            external_code="1e",
        )
        cls.pharmacy_dimfarm = PharmacyModelFactory(
            distributor=cls.distributor_dimfarm,
            external_code="1d",
        )

    @override_storage()
    @patch.object(FileRepository, "read_file_binary")
    @patch("os.path.isfile")
    @patch("os.path.exists")
    @patch.object(XMLFile, "read_order_dimfarm")
    @patch.object(DBFFileV2, "read_order_eapteka_v2")
    @patch.object(XMLFile, "read")
    @patch.object(DBFFileV2, "read_order_ufarma_v2")
    @patch.object(FTPServerV1, "download_all_files")
    @patch.object(FTPServerV1, "get_order_files_list")
    def test_get_orders(
        self,
        mock_get_order_files_list,
        mock_download_all_files,
        mock_read_order_ufarma,
        mock_read_smart_apteka,
        mock_read_order_eapteka_v2,
        mock_read_order_dimfarm,
        mock_exists,
        mock_isfile,
        mock_read_file_binary,
    ):
        orders = Order.objects.all()
        assert len(orders) == 0
        mock_get_order_files_list.return_value = []
        mock_download_all_files.return_value = [
            "tmp_folder/uuid_folder_name/ufarma/file_name.dbf",
            "tmp_folder/uuid_folder_name/smart_apteka/file_name.xml",
            "tmp_folder/uuid_folder_name/eapteka/file_name.txt",
            "tmp_folder/uuid_folder_name/dimfarm/file_name.txt",
        ]
        mock_read_order_ufarma.return_value = [
            {
                "numz": "123",
                "date": "2020-01-01",
                "datez": "2020-01-01",
                "code": "123",
                "name": "Name",
                "qtty": 7.0,
                "podrcd": self.pharmacy_ufarma.external_code,
                "price": 123.0,
                "podr": "podr_ufarma",
                "md": "123",
            },
            {
                "numz": "123",
                "date": "2020-01-01",
                "datez": "2020-01-01",
                "code": "123",
                "name": "Name2",
                "qtty": 8.0,
                "podrcd": self.pharmacy_ufarma.external_code,
                "price": 123.0,
                "podr": "podr_ufarma",
                "md": "123",
            },
        ]
        mock_read_smart_apteka.return_value = {
            "PACKET": {
                "@TYPE": "11",
                "@NAME": "Заказ поставщику",
                "@ID": "27722001",
                "@PRED_ID": "13",
                "@FROM": "000130001",
                "@TO": "13785",
                "@DB_VER": "1240",
                "@EXE_VER": "1.0.0.43",
                "ORDER": {
                    "ORDER_ID": "123",
                    "CLIENT_ID": self.pharmacy_smart_apteka.external_code,
                    "DEP_ID": "1011",
                    "REPLY_TO": "000130001",
                    "ORDERDATE": "02.02.2018 15:45:02",
                    "PLDATE": "02.02.2018 15:30:41",
                    "PL_NAME": "ООО",
                    "PAYTYPE": "Отсрочка0",
                    "ITEMS": {
                        "ITEM": [
                            {
                                "CODE": "64932318",
                                "NAME": "N60",
                                "VENDOR": "КВАЙССЕР ФАРМА ГМБХ И КО. КГ",
                                "QTTY": "1",
                                "PRICE": "249,84",
                            },
                            {
                                "CODE": "611304666",
                                "NAME": "N 14",
                                "VENDOR": "ХИМИКО-ФАРМАЦЕВТИЧЕСКИЙ ЗАВОД",
                                "QTTY": "1",
                                "PRICE": "300,33",
                            },
                            {
                                "CODE": "696722934",
                                "NAME": "50Г N 1",
                                "VENDOR": "РЕКИТТ БЕНЗИКЕР ХЕЛСКЭР ЛИМИТЕД",
                                "QTTY": "2",
                                "PRICE": "134,58",
                            },
                            {
                                "CODE": "85613469",
                                "NAME": "N 14",
                                "VENDOR": "МЕРК ШАРП И ДОУМ ЛТД/АКРИХИН ОАО",
                                "QTTY": "2",
                                "PRICE": "62,78",
                            },
                            {
                                "CODE": "548781734",
                                "NAME": "15МЛ N 1",
                                "VENDOR": "УРСАФАРМ АРЦНАЙМИТТЕЛЬ ГМБХ",
                                "QTTY": "20",
                                "PRICE": "124,4",
                            },
                            {
                                "CODE": "58783389",
                                "NAME": "N 10",
                                "VENDOR": "НОВАРТИС УРУНЛЕРИ",
                                "QTTY": "1",
                                "PRICE": "191,96",
                            },
                        ],
                    },
                },
            },
        }
        mock_read_order_eapteka_v2.return_value = [
            {
                "numz": "123",
                "datez": datetime(2020, 1, 1),
                "code": "123",
                "date": datetime(2020, 1, 1),
                "name": "Name",
                "podr": "podr_eapteka",
                "qtty": 7.0,
                "price": 123.0,
                "podrcd": self.pharmacy_eapteka.external_code,
                "ean13": "1111111111111",
                "zak_ustr1": False,
            }
        ]
        mock_read_order_dimfarm.return_value = {
            "PACKET": {
                "@TYPE": "11",
                "@NAME": "Заказ поставщику",
                "@ID": "27722001",
                "@PRED_ID": "13",
                "@FROM": "000130001",
                "@TO": "13785",
                "@DB_VER": "1240",
                "@EXE_VER": "1.0.0.43",
                "ORDER": {
                    "ORDER_ID": "123",
                    "CLIENT_ID": self.pharmacy_dimfarm.external_code,
                    "DEP_ID": "1011",
                    "REPLY_TO": "000130001",
                    "ORDERDATE": "02.02.2018 15:45:02",
                    "PLDATE": "02.02.2018 15:30:41",
                    "PL_NAME": "ООО",
                    "PAYTYPE": "Отсрочка0",
                    "ITEMS": {
                        "ITEM": [
                            {
                                "CODE": "611304666",
                                "NAME": "N 14",
                                "VENDOR": "ХИМИКО-ФАРМАЦЕВТИЧЕСКИЙ ЗАВОД",
                                "QTTY": "1",
                                "PRICE": "300,33",
                            },
                            {
                                "CODE": "696722934",
                                "NAME": "50Г N 1",
                                "VENDOR": "РЕКИТТ БЕНЗИКЕР ХЕЛСКЭР ЛИМИТЕД",
                                "QTTY": "2",
                                "PRICE": "134,58",
                            },
                            {
                                "CODE": "85613469",
                                "NAME": "N 14",
                                "VENDOR": "МЕРК ШАРП И ДОУМ ЛТД/АКРИХИН ОАО",
                                "QTTY": "2",
                                "PRICE": "62,78",
                            },
                            {
                                "CODE": "548781734",
                                "NAME": "15МЛ N 1",
                                "VENDOR": "УРСАФАРМ АРЦНАЙМИТТЕЛЬ ГМБХ",
                                "QTTY": "20",
                                "PRICE": "124,4",
                            },
                            {
                                "CODE": "58783389",
                                "NAME": "N 10",
                                "VENDOR": "НОВАРТИС УРУНЛЕРИ",
                                "QTTY": "1",
                                "PRICE": "191,96",
                            },
                        ],
                    },
                },
            },
        }
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_read_file_binary.return_value = b"test"
        uc = GetOrdersUseCase(
            ftp_service=FTPORMServiceV1(),
            ftp_server=FTPServerV1(),
            pharmacy_service=PharmacyServiceV1(),
            order_item_service=OrderItemServiceV1(),
            order_status_service=OrderStatusServiceV1(),
            file_service=FileServiceV1(),
            cache_service=CacheService,
            log_service=LogServiceV1(),
        )
        uc.process_orders()

        orders = Order.objects.all()
        assert len(orders) == 4

        order_ufarma = Order.objects.get(
            numz="123", distributor=self.distributor_ufarma
        )
        assert order_ufarma.distributor.id == self.distributor_ufarma.id
        assert order_ufarma.numz == "123"
        assert order_ufarma.podrcd == self.pharmacy_ufarma.external_code
        assert order_ufarma.podr == "podr_ufarma"

        order_items_ufarma = order_ufarma.items.all()
        assert len(order_items_ufarma) == 2

        order_smart = Order.objects.get(
            numz="123", distributor=self.distributor_smart_apteka
        )
        assert order_smart.distributor.id == self.distributor_smart_apteka.id
        assert order_smart.numz == "123"
        assert order_smart.podrcd == self.pharmacy_smart_apteka.external_code

        order_items_smart = order_smart.items.all()
        assert len(order_items_smart) == 6

        order_eapteka = Order.objects.get(
            numz="123", distributor=self.distributor_eapteka
        )
        assert order_eapteka.distributor.id == self.distributor_eapteka.id
        assert order_eapteka.numz == "123"
        assert order_eapteka.podrcd == self.pharmacy_eapteka.external_code
        assert order_eapteka.podr == "podr_eapteka"

        order_items_eapteka = order_eapteka.items.all()
        assert len(order_items_eapteka) == 1

        order_dimfarm = Order.objects.get(
            numz="123", distributor=self.distributor_dimfarm
        )
        assert order_dimfarm.distributor.id == self.distributor_dimfarm.id
        assert order_dimfarm.numz == "123"
        assert order_dimfarm.podrcd == self.pharmacy_dimfarm.external_code

        order_items_dimfarm = order_dimfarm.items.all()
        assert len(order_items_dimfarm) == 5
