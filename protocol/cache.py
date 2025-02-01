from typing import Any, Protocol


class CacheServiceProtocol(Protocol):
    def get(self, key: str) -> Any:
        """Получает значение из кеша"""
        pass

    def set(self, key: str, value: Any, timeout: int) -> None:
        """Сохраняет значение в кеш"""
        pass
