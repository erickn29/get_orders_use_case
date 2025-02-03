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
    # TODO подумать над тем, чтобы разделить класс на несколько сценариев
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
        self._ftp_service = ftp_service
        self._ftp_server = ftp_server
        self._pharmacy_service = pharmacy_service
        self._order_item_service = order_item_service
        self._order_status_service = order_status_service
        self._file_service = file_service
        self._cache_service = cache_service
        self._log_service = log_service

    def process_orders(self):
        """Получает заказы с ФТП серверов дистрибьюторов и обрабатывает их"""
        local_order_files = self._get_order_files_from_ftp()
        for file_path in local_order_files:
            protocol = self._get_ftp_protocol_by_file_path(file_path)
            if not protocol or protocol not in Distributor.Protocol.labels:
                self._alert_tg(f"Не найден протокол для создания заказов: {protocol}")
                continue
            order_service = OrderService(protocol=protocol)
            order, is_created = self._create_order_and_items(file_path, order_service)
            if not order:
                continue
            # TODO выполнить действия в методе get_or_create
            self._create_order_status(order, OrderStatus.Status.NEW, file_path)
            file = self._file_service.create(file_path, file_path.split("/")[-1])
            order_service.add_file_to_order(order, file)

    def _get_order_files_from_ftp(self) -> list[str]:
        """
        Загружает файлы заказа с фтп серверов в локальную папку.
        Возвращает список путей к файлам заказа.
        """
        ftp_objects: list[FTP] = self._ftp_service.get_all()
        local_order_files: list[str] = []
        for ftp in ftp_objects:
            ftp_files: list[str] = self._ftp_server.get_order_files_list(ftp)
            local_files: list[str] = self._ftp_server.download_all_files(ftp, ftp_files)
            local_order_files.extend(local_files)
        return local_order_files

    def _get_ftp_protocol_by_file_path(self, path: str) -> str | None:
        """Получает протокол по пути для заказа"""
        path_items_count = 4
        order_path_to_list = path.split("/")
        if len(order_path_to_list) != path_items_count:
            self._alert_tg(f"Неверный формат пути для заказа '{path}'")
            return
        return path.split("/")[2]

    def _alert_tg(self, msg: str):
        self._log_service.log(msg, to_sentry=False)

    def _get_distributor_by_pharmacy(self, podrcd: str) -> Distributor | None:
        """Сопоставляет подразделение (код аптеки) с дистрибьютором"""
        if pharmacy := self._pharmacy_service.find(external_code=podrcd):
            return pharmacy.distributor
        self._alert_tg(f"Не найдена аптека с кодом '{podrcd}'")

    def _create_order_and_items(
        self, order_file: str, order_service: OrderService
    ) -> tuple[Order | None, bool]:
        """Создает заказ в БД из локального файла"""
        order_schema_list = order_service.read_order_from_local_file(order_file)
        if not order_schema_list:
            self._alert_tg(f"Нет данных для создания заказа: '{order_file}'")
            return None, False
        distributor = self._get_distributor_by_pharmacy(order_schema_list[0].podrcd)
        if not distributor:
            self._alert_tg(f"Не найден дистрибьютор заказа '{order_file}'")
            return None, False
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
        self._create_order_items(order, order_schema_list)
        return order, is_created

    def _create_order_items(self, order: Order, orders: list[OrderSchemaFromFile]):
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
            self._order_item_service.get_or_create(order=order, order_item=schema)

    def _create_order_status(self, order: Order, status: OrderStatus.Status, path: str):
        """Создает объект статуса заказа в БД"""
        self._order_status_service.create(order, status)
        if not self._cache_service.get(f"order:{order.distributor.title}:{order.numz}"):
            self._alert_tg(
                f"ЗАКАЗ\n"
                f"Дистрибьютор: {order.distributor}\n"
                f"Получен новый заказ {path.split('/')[-1]}"
            )
            self._cache_service.set(
                key=f"order:{order.distributor.title}:{order.numz}",
                value=1,
                timeout=60 * 60 * 24,
            )
