from typing import TypeVar

from django.db.models import Model


T = TypeVar("T", bound=Model)


class BaseDjangoRepository:
    model: T = None

    def create(self, **data) -> T:
        return self.model.objects.create(**data)

    def get(self, **filters) -> T:
        return self.model.objects.get(**filters)

    def get_or_create(self, **data) -> tuple[T, bool]:
        return self.model.objects.get_or_create(**data)

    def filter(self, **filters) -> list[T]:
        return self.model.objects.filter(**filters)

    def find(self, **filters) -> T | None:
        return self.model.objects.filter(**filters).first()

    def get_all(self) -> list[T]:
        return self.model.objects.all()

    def delete(self, obj: T):
        return obj.delete()
