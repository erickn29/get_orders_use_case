from order.models import OrderItem
from order.repository.base_django import BaseDjangoRepository


class OrderItemRepository(BaseDjangoRepository):
    model = OrderItem
