import os

from django.core.files.base import ContentFile

from filemanager.models import File
from order.repository.base_django import BaseDjangoRepository
from utils.other import log


class FileRepository(BaseDjangoRepository):
    model = File

    @staticmethod
    def read_file_binary(path_to_file: str) -> bytes | None:
        """Метод читает файл в байты"""
        if not os.path.isfile(path_to_file):
            log(f"ERROR FILE\nФайл не найден {path_to_file}")
            return
        with open(path_to_file, mode="rb") as f:
            file_bytes = f.read()
        return file_bytes

    def create(self, path_to_file: str, file_name_db: str) -> File | None:
        content = self.read_file_binary(path_to_file)
        if not content:
            return
        file = File(
            title=file_name_db.split(".")[0],
            extension=file_name_db.split(".")[-1],
        )
        file.file = ContentFile(content=content, name=f"{file.title}.{file.extension}")
        file.save()
        return file
