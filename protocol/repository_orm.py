from typing import Protocol, TypeVar


T = TypeVar("T")


class ORMRepositoryProtocol(Protocol):
    model: T = None

    def create(self, **data) -> T:
        pass

    def get_or_create(self, **data) -> tuple[T, bool]:
        pass

    def get(self, **filters) -> T:
        pass

    def filter(self, **filters) -> list[T]:
        pass

    def find(self, **filters) -> T | None:
        pass

    def get_all(self) -> list[T]:
        pass

    def delete(self, obj: T):
        pass
