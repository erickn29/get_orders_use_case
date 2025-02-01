from typing import Protocol

from order.models import Order, OrderStatus
from order.repository.order_status import OrderStatusRepository


class OrderStatusServiceProtocol(Protocol):
    def create(self, order: Order, status: OrderStatus.Status) -> OrderStatus:
        """Создает объект статуса заказа в БД"""
        pass


class OrderStatusServiceV1:
    repository = OrderStatusRepository

    def create(self, order: Order, status: OrderStatus.Status) -> OrderStatus:
        """Создает объект статуса заказа в БД"""
        return self.repository().create(order=order, status=status)
