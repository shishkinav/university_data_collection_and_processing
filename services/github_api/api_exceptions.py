class APIConnectionError(Exception):
    """
    Ошибки соединения с API GitHub
    """
    def __init__(self, message: str):
        self.detail = message

    def __str__(self):
        return f'Ошибка соединения: {self.detail}'


class APIRequestFail(Exception):
    """
    Ошибки запросов к API GitHub
    """
    def __init__(self, message: str):
        self.detail = message

    def __str__(self):
        return f'Запрос к API некорректен: {self.detail}'
