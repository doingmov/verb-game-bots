import logging

import requests


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token: str, chat_id: str):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        try:
            requests.post(
                f'https://api.telegram.org/bot{self.token}/sendMessage',
                data={'chat_id': self.chat_id, 'text': message},
                timeout=10,
            )
        except requests.RequestException:
            pass