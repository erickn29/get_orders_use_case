from typing import Protocol


class TelegramBotProtocol(Protocol):
    def send_message(self, message: str, chat_id: int) -> bool:
        """Send message to Telegram"""
        pass

    def handler_request(
        self, path: str, method: str = "GET", params: dict = None
    ) -> bool:
        """Метод отправляет запрос в телеграм"""
        pass

    @staticmethod
    def __handler_error(response) -> bool:
        """Обработка ошибок отправки сообщения в телеграм"""
        pass
