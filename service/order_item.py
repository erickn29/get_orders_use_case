from typing import Protocol

from order.models import Order, OrderItem
from order.repository.order_item import OrderItemRepository
from order.schema.order import OrderItemSchema


class OrderItemServiceProtocol(Protocol):
    def get_or_create(
        self, order: Order, order_item: OrderItemSchema
    ) -> tuple[OrderItem, bool]:
        """Получает или создает заказ в БД"""
        pass


class OrderItemServiceV1:
    repository = OrderItemRepository

    def get_or_create(
        self, order: Order, order_item: OrderItemSchema
    ) -> tuple[OrderItem, bool]:
        return self.repository().get_or_create(order=order, **order_item.model_dump())
