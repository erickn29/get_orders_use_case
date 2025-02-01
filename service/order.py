from filemanager.models import File
from order.models import Distributor, Order
from order.protocol.repository_main import OrderRepositoryProtocol
from order.repository.order import UfarmaOrderRepository
from order.schema.order import OrderSchema, OrderSchemaFromFile
from utils.other import log


class OrderService:

    def __init__(self, protocol: str):
        self.protocol = protocol
        self.repo: OrderRepositoryProtocol = self.__get_repository()

    def __get_repository(self):
        repositories = {
            Distributor.Protocol.UFARMA: UfarmaOrderRepository,
            Distributor.Protocol.DIMFARM: None,
            Distributor.Protocol.EAPTEKA: None,
            Distributor.Protocol.SMART_APTEKA: None,
        }
        repository = repositories.get(self.protocol)
        if not repository:
            msg = f"Не найден репозиторий для протокола '{self.protocol}'"
            log(msg)
            raise ValueError(msg)
        return repository()

    def read_order_from_local_file(
        self, path_to_file: str
    ) -> list[OrderSchemaFromFile] | None:
        """Читает файл заказа"""
        orders = self.repo.read_order_from_local_file(path_to_file)
        return orders

    def create(self, distributor: Distributor, order_schema: OrderSchema) -> Order:
        """Сохраняет заказ в БД"""
        return self.repo.create(distributor=distributor, **order_schema.model_dump())

    def get_or_create(
        self, distributor: Distributor, order_schema: OrderSchema
    ) -> tuple[Order, bool]:
        """Сохраняет заказ в БД или получает его из БД"""
        return self.repo.get_or_create(
            distributor=distributor, **order_schema.model_dump()
        )

    def add_file_to_order(self, order: Order, file: File):
        """Добавляет файл к заказу"""
        if not file:
            log(f"ERROR FILE\nНе удалось сохранить файл заказа {order.numz} в БД")
            return
        self.repo.add_file_to_order(order, file)
