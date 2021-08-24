import scrapy


class BaseSpider(scrapy.Spider):
    """
    Базовый класс для других пауков. Отдельно не может существовать,
        так как определяет не вся основные атрибуты родителя.
    Отвечает за расширение исходных данных паука:
        можно указать start_urls с переменной {target} в пути и
        передать target (поисковый запрос при инициализации)
    """
    def __init__(self, *args, target: str = None, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        if target is not None:
            self.target = target
            self.start_urls = [_.format(target=target) for _ in self.start_urls]
        if not hasattr(self, 'converter'):
            raise ValueError(f'{type(self).__name__} must have a converter')

