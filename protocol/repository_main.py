from filemanager.models import File
from order.models import Order
from order.protocol.repository_file import FileRepositoryProtocol
from order.protocol.repository_orm import ORMRepositoryProtocol


class RepositoryProtocol(ORMRepositoryProtocol, FileRepositoryProtocol):
    pass


class OrderRepositoryProtocol(RepositoryProtocol):
    def add_file_to_order(self, order: Order, file: File):
        """Добавляет файл к заказу"""
        pass
