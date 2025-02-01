from typing import Protocol

from filemanager.models import File
from order.repository.file import FileRepository


class FileServiceProtocol(Protocol):

    def read_file_binary(self, path_to_file: str) -> bytes | None:
        """Метод читает файл в байты"""
        pass

    def create(self, path_to_file: str, file_name_db: str) -> File | None:
        """Метод создает объект файла в БД и возвращает его"""
        pass


class FileService:
    repository = FileRepository

    def read_file_binary(self, path_to_file: str) -> bytes | None:
        """Метод читает файл в байты"""
        return self.repository.read_file_binary(path_to_file)

    def create(self, path_to_file: str, file_name_db: str) -> File | None:
        """Метод создает объект файла в БД и возвращает его"""
        return self.repository().create(path_to_file, file_name_db)
