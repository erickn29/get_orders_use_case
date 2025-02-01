from typing import Protocol


class LogServiceProtocol(Protocol):
    def log(self, msg: str, level: str = "error", to_sentry: bool = True):
        """Отправляет сообщение в телеграм и отправляет его в sentry"""
        pass
