import os

from abc import ABC, abstractmethod

from filemanager.models import File
from filemanager.services.dbf_file import DBFFileV2
from filemanager.services.xml_file import XMLFile
from order.models import Order
from order.repository.base_django import BaseDjangoRepository
from order.schema.order import OrderSchemaFromFile
from utils.other import log, string_to_float, switch_date_string

from pydantic import ValidationError


class BaseOrderRepository(BaseDjangoRepository, ABC):
    model = Order

    @abstractmethod
    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile] | None:
        raise NotImplementedError

    @staticmethod
    def add_file_to_order(order: Order, file: File):
        """Добавляет файл к заказу"""
        order.file = file
        order.save()


class XmlOrderTypeRepository:
    read_order_method_name = None


class UfarmaOrderRepository(BaseOrderRepository):

    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile] | None:
        if not os.path.exists(path):
            log(f"Не найден путь заказа '{path}'")
            return
        orders: list[dict] = DBFFileV2(path).read_order_ufarma_v2()
        try:
            return [OrderSchemaFromFile(**order) for order in orders]
        except ValidationError as err:
            log(f"Ошибка валидации заказа [{path}] '{str(err)}'")


class EaptekaOrderRepository(BaseOrderRepository):

    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile] | None:
        if not os.path.exists(path):
            log(f"Не найден путь заказа '{path}'")
            return
        orders: list[dict] = DBFFileV2(path).read_order_eapteka_v2()
        try:
            return [OrderSchemaFromFile(**order) for order in orders]
        except ValidationError as err:
            log(f"Ошибка валидации заказа [{path}] '{str(err)}'")


class SmartAptekaOrderRepository(BaseOrderRepository):
    read_order_method_name = "read"

    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile] | None:
        if not os.path.exists(path):
            log(f"Не найден путь заказа '{path}'")
            return
        order_schema_list = []
        order: dict = XMLFile(path).read()
        order_dict = {
            "numz": order["PACKET"]["ORDER"].get("ORDER_ID"),
            "datez": switch_date_string(order["PACKET"]["ORDER"].get("ORDERDATE")),
            "date": switch_date_string(order["PACKET"]["ORDER"].get("PLDATE")),
            "podrcd": order["PACKET"]["ORDER"].get("CLIENT_ID"),
        }
        order_item: dict | list[dict] = order["PACKET"]["ORDER"]["ITEMS"]["ITEM"]
        if isinstance(order_item, list):
            for item in order_item:
                order_schema_list.append(
                    OrderSchemaFromFile(
                        **{
                            **order_dict,
                            **{
                                "code": item.get("CODE"),
                                "name": item.get("NAME"),
                                "qtty": item.get("QTTY"),
                                "price": string_to_float(item.get("PRICE")),
                            },
                        }
                    )
                )
        else:
            order_schema_list.append(
                OrderSchemaFromFile(
                    **{
                        **order_dict,
                        **{
                            "code": order_item.get("CODE"),
                            "name": order_item.get("NAME"),
                            "qtty": order_item.get("QTTY"),
                            "price": string_to_float(order_item.get("PRICE")),
                        },
                    }
                )
            )
        return order_schema_list


class DimfarmOrderRepository(BaseOrderRepository):
    read_order_method_name = "read_order_dimfarm"

    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile] | None:
        if not os.path.exists(path):
            log(f"Не найден путь заказа '{path}'")
            return
        order_schema_list = []
        order: dict = XMLFile(path).read_order_dimfarm()
        order_dict = {
            "numz": order["PACKET"]["ORDER"].get("ORDER_ID"),
            "datez": switch_date_string(order["PACKET"]["ORDER"].get("ORDERDATE")),
            "date": switch_date_string(order["PACKET"]["ORDER"].get("PLDATE")),
            "podrcd": order["PACKET"]["ORDER"].get("CLIENT_ID"),
        }
        order_item: dict | list[dict] = order["PACKET"]["ORDER"]["ITEMS"]["ITEM"]
        if isinstance(order_item, list):
            for item in order_item:
                order_schema_list.append(
                    OrderSchemaFromFile(
                        **{
                            **order_dict,
                            **{
                                "code": item.get("CODE"),
                                "name": item.get("NAME"),
                                "qtty": item.get("QTTY"),
                                "price": string_to_float(item.get("PRICE")),
                            },
                        }
                    )
                )
        else:
            order_schema_list.append(
                OrderSchemaFromFile(
                    **{
                        **order_dict,
                        **{
                            "code": order_item.get("CODE"),
                            "name": order_item.get("NAME"),
                            "qtty": order_item.get("QTTY"),
                            "price": string_to_float(order_item.get("PRICE")),
                        },
                    }
                )
            )
        return order_schema_list
