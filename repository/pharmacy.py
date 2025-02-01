from order.models import Pharmacy
from order.repository.base_django import BaseDjangoRepository


class PharmacyRepository(BaseDjangoRepository):
    model = Pharmacy
