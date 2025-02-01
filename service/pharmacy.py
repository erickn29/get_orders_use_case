from typing import Protocol

from order.models import Pharmacy
from order.repository.pharmacy import PharmacyRepository


class PharmacyServiceProtocol(Protocol):
    def find(self, **filters) -> Pharmacy | None:
        """Поиск аптеки по фильтрам"""
        pass


class PharmacyService:
    repository = PharmacyRepository

    def __init__(self):
        self.repo = self.repository()

    def find(self, **filters) -> Pharmacy | None:
        return self.repo.find(**filters)
