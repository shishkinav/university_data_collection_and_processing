class BSConnectionError(Exception):
    """
    Ошибки соединений и таймауты при внешних запросах
    """
    def __init__(self, message: str):
        self.detail = message

    def __str__(self):
        return f'Ошибка соединения: {self.detail}'


class BSRequestFail(Exception):
    """
    Ошибки запросов парсинга
    """
    def __init__(self, status_code: int, message: str):
        self.status = status_code
        self.detail = message

    def __str__(self):
        return f'Запрос на парсинг fail: status - {self.status}; error - {self.detail}'


class BSParseError(Exception):
    """
    Ошибки соединений и таймауты при внешних запросах
    """
    def __init__(self, message: str):
        self.detail = message

    def __str__(self):
        return f'Ошибка парсинга данных: {self.detail}'
