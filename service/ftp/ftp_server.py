import os
import uuid

from typing import Protocol

from backend import settings
from order.models import FTP
from utils.ftp_server import FTPServer


class FTPServerProtocol(Protocol):
    def __get_server(self, ftp: FTP):
        pass

    def __get_local_filepath(self, ftp: FTP, file_name: str):
        pass

    def upload_file(self, file_path: str, file_name: str) -> bool:
        """Загружает файл на сервер в папку по указанному пути"""
        pass

    def get_order_files_list(self, ftp: FTP) -> list[str]:
        """Получает список файлов в папке на сервере"""
        pass

    def download_all_files(self, ftp: FTP, files: list[str]) -> list[str]:
        """Скачивает файлы с сервера в локальный путь.
        Принимает список путей к файлам в сервере.
        Возвращает список путей к скачанным файлам
        """
        pass

    def download_file(self, ftp: FTP, ftp_path: str) -> str:
        """Скачивает файл из сервера в локальный путь"""
        pass

    def delete_file(self, file_path: str):
        """Удаляет файл с сервера"""
        pass


class FTPServerV1:
    server = FTPServer

    def __get_server(self, ftp: FTP):
        server = self.server(ftp.host, ftp.username, ftp.password)
        return server

    @staticmethod
    def __get_local_filepath(ftp: FTP, file_name: str):
        """Генерирует локальный путь для загрузки файла с сервера"""
        tmp_folder = settings.TMP_FILES_DIR
        uuid_folder_name = uuid.uuid4().hex
        os.mkdir(f"{tmp_folder}/{uuid_folder_name}/{ftp.protocol}/{file_name}")
        return f"{tmp_folder}/{uuid_folder_name}/{ftp.protocol}/{file_name}"

    def upload_file(self, file_path, file_name):
        """Загружает файл на сервер в папку по указанному пути"""
        pass

    def get_order_files_list(self, ftp: FTP) -> list[str]:
        """Получает список файлов в папке на сервере"""
        server = self.__get_server(ftp)
        return server.ls(ftp.path_order)

    def download_all_files(self, ftp: FTP, files: list[str]) -> list[str]:
        """Скачивает файлы с сервера в локальный путь.
        Принимает список путей к файлам в сервере.
        Возвращает список путей к скачанным файлам
        """
        files_downloaded = []
        for file in files:
            local_path = self.download_file(ftp, file)
            files_downloaded.append(local_path)
        return files_downloaded

    def download_file(self, ftp: FTP, ftp_path: str) -> str:
        """Скачивает файл из сервера в локальный путь"""
        server = self.__get_server(ftp)
        file_name = ftp_path.split("/")[-1]
        return server.download_file(ftp_path, self.__get_local_filepath(ftp, file_name))

    def delete_file(self, file_path: str):
        """Удаляет файл с сервера"""
        pass
