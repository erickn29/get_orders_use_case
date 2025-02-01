from order.models import FTP, Distributor, Order, OrderStatus
from order.protocol.cache import CacheServiceProtocol
from order.protocol.log import LogServiceProtocol
from order.schema.order import OrderItemSchema, OrderSchema, OrderSchemaFromFile
from order.service.file import FileServiceProtocol
from order.service.ftp.ftp_orm import FTPORMServiceProtocol
from order.service.ftp.ftp_server import FTPServerProtocol
from order.service.order import OrderService
from order.service.order_item import OrderItemServiceProtocol
from order.service.order_status import OrderStatusServiceProtocol
from order.service.pharmacy import PharmacyServiceProtocol


class GetOrdersUseCase:
    def __init__(
        self,
        ftp_service: FTPORMServiceProtocol,
        ftp_server: FTPServerProtocol,
        pharmacy_service: PharmacyServiceProtocol,
        order_item_service: OrderItemServiceProtocol,
        order_status_service: OrderStatusServiceProtocol,
        file_service: FileServiceProtocol,
        cache_service: CacheServiceProtocol,
        log_service: LogServiceProtocol,
    ):
        self.ftp_service = ftp_service
        self.ftp_server = ftp_server
        self.pharmacy_service = pharmacy_service
        self.order_item_service = order_item_service
        self.order_status_service = order_status_service
        self.file_service = file_service
        self.cache_service = cache_service
        self.log_service = log_service

    def __alert_tg(self, msg: str):
        self.log_service.log(msg, to_sentry=False)

    def __get_order_files_from_ftp(self) -> list[str]:
        """
        Загружает файлы заказа с фтп серверов в локальную папку.
        Возвращает список путей к файлам заказа.
        """
        ftp_objects: list[FTP] = self.ftp_service.get_all()
        local_order_files: list[str] = []
        for ftp in ftp_objects:
            ftp_files: list[str] = self.ftp_server.get_order_files_list(ftp)
            local_files: list[str] = self.ftp_server.download_all_files(ftp, ftp_files)
            local_order_files.append(*local_files)
        return local_order_files

    def __get_ftp_protocol_by_file_path(self, path: str) -> str | None:
        """Получает протокол по пути для заказа"""
        path_items_count = 4
        order_path_to_list = path.split("/")
        if len(order_path_to_list) != path_items_count:
            self.__alert_tg(f"Неверный формат пути для заказа '{path}'")
            return
        return path.split("/")[2]

    def __get_distributor_by_pharmacy(self, podrcd: str) -> Distributor | None:
        """Сопоставляет подразделение (код аптеки) с дистрибьютором"""
        if pharmacy := self.pharmacy_service.find(external_code=podrcd):
            return pharmacy.distributor
        self.__alert_tg(f"Не найдена аптека с кодом '{podrcd}'")

    def __create_order_and_items(
        self, order_file: str, order_service: OrderService
    ) -> tuple[Order, bool] | None:
        """Создает заказ в БД из локального файла"""
        order_schema_list = order_service.read_order_from_local_file(order_file)
        if not order_schema_list:
            self.__alert_tg(f"Нет данных для создания заказа: '{order_file}'")
            return
        distributor = self.__get_distributor_by_pharmacy(order_schema_list[0].podrcd)
        if not distributor:
            self.__alert_tg(f"Не найден дистрибьютор заказа '{order_file}'")
            return
        order_schema = OrderSchema(
            numz=order_schema_list[0].numz,
            datez=order_schema_list[0].datez,
            date=order_schema_list[0].date,
            podr=order_schema_list[0].podr,
            podrcd=order_schema_list[0].podrcd,
            md=order_schema_list[0].md,
            partn=order_schema_list[0].partn,
            zak_ustr1=order_schema_list[0].zak_ustr1,
        )
        order, is_created = order_service.get_or_create(
            order_schema=order_schema,
            distributor=distributor,
        )
        self.__create_order_items(order, order_schema_list)
        return order, is_created

    def __create_order_items(self, order: Order, orders: list[OrderSchemaFromFile]):
        """Создает заказ в БД из локального файла"""
        for order_item in orders:
            schema = OrderItemSchema(
                code=order_item.code,
                name=order_item.name,
                qtty=order_item.qtty,
                price=order_item.price,
                vendor=order_item.vendor,
                ean13=order_item.ean13,
            )
            self.order_item_service.get_or_create(order=order, order_item=schema)

    def __create_order_status(
        self, order: Order, status: OrderStatus.Status, path: str
    ):
        """Создает объект статуса заказа в БД"""
        self.order_status_service.create(order, status)
        if not self.cache_service.get(f"order:{order.distributor.title}:{order.numz}"):
            self.__alert_tg(
                f"ЗАКАЗ\n"
                f"Дистрибьютор: {order.distributor}\n"
                f"Получен новый заказ {path.split('/')[-1]}"
            )
            self.cache_service.set(
                key=f"order:{order.distributor.title}:{order.numz}",
                value=1,
                timeout=60 * 60 * 24,
            )

    def process_orders(self):
        """Обрабатывает полученные заказы из локальной папки"""
        local_order_files = self.__get_order_files_from_ftp()
        for file_path in local_order_files:
            protocol = self.__get_ftp_protocol_by_file_path(file_path)
            if not protocol or protocol not in Distributor.Protocol.labels:
                self.__alert_tg(f"Не найден протокол для создания заказов: {protocol}")
                continue
            order_service = OrderService(protocol=protocol)
            order, is_created = self.__create_order_and_items(file_path, order_service)
            if not is_created:
                continue
            self.__create_order_status(order, OrderStatus.Status.NEW, file_path)
            file = self.file_service.create(file_path, file_path.split("/")[-1])
            order_service.add_file_to_order(order, file)
