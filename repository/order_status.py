from order.models import OrderStatus
from order.repository.base_django import BaseDjangoRepository


class OrderStatusRepository(BaseDjangoRepository):
    model = OrderStatus
