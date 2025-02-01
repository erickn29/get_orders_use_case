from typing import Protocol

from order.schema.order import OrderSchemaFromFile


class FileRepositoryProtocol(Protocol):
    def read_order_from_local_file(self, path: str) -> list[OrderSchemaFromFile]:
        """Читает файл заказа"""
        pass
