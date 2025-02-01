import os

from abc import ABC, abstractmethod

from filemanager.models import File
from filemanager.services.dbf_file import DBFFileV2
from order.models import Order
from order.repository.base_django import BaseDjangoRepository
from order.schema.order import OrderSchemaFromFile
from utils.other import log

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


class UfarmaOrderRepository(BaseOrderRepository):

    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile] | None:
        if not os.path.exists(path):
            log(f"Не найден путь заказа '{path}'")
            return
        orders: list[dict] = DBFFileV2(path).read_order_ufarma()
        try:
            return [OrderSchemaFromFile(**order) for order in orders]
        except ValidationError as err:
            log(f"Ошибка валидации заказа [{path}] '{str(err)}'")
