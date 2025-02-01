from order.models import FTP
from order.repository.base_django import BaseDjangoRepository


class FTPRepository(BaseDjangoRepository):
    model = FTP
