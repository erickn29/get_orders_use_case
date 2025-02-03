from typing import Protocol

from order.models import FTP
from order.repository.ftp import FTPRepository


class FTPORMServiceProtocol(Protocol):
    def __init__(self):
        pass

    def get_all(self) -> list[FTP]:
        """Получает все фтп из БД"""
        pass


class FTPORMServiceV1:
    repository = FTPRepository

    def __init__(self):
        self.repo = self.repository()

    def get_all(self) -> list[FTP]:
        """Получает все фтп из БД"""
        return self.repo.get_all()


ftp_service_v1 = FTPORMServiceV1()
