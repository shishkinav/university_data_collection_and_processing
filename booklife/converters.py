from abc import ABC, abstractmethod
import hashlib
from booklife import items
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from decimal import Decimal, ROUND_HALF_UP

class BaseConverter(ABC):
    @abstractmethod
    def prepare_data(self, item) -> dict:
        """
        Обязательный метод, отвечающий за подготовку Item
            перед сохранением в БД
        """
        pass

    @abstractmethod
    def parse_data(self, item) -> dict:
        """
        Обязательный метод, отвечающий за базовый парсинг
            данных для полей Item
        """
        pass


class LabirintItemConverter(BaseConverter):
    """
    Класс обработчик данных Item для labirint.ru
    """
    def prepare_data(self, item: items.BooklifeItem) -> items.BooklifeItem:
        item['name'] = " ".join(item["name"].split(": ")[1:])
        # item.name = " ".join(str(item.name).split(": ")[1:])
        item["rate"] = float(item["rate"])
        item["_id"] = hashlib.sha1(str(item).encode()).hexdigest()
        return item

    def parse_data(self, item) -> dict:
        pass


class LeroyMerlinItemConverter(BaseConverter):
    """
    Класс обработчик данных Item для leroymerlin.ru
    """
    def prepare_data(self, item: items.BooklifeItem) -> items.LeroyMerlinItem:
        """
        Финальное преобразование полей item
        """
        item['price'] = float(item['price'])
        return item

    def parse_data(self, response: HtmlResponse):
        """
        Парсинг данных для item:
            ● название;
            ● все фото;
            ● параметры товара в объявлении;
            ● ссылка;
            ● цена.
        """
        loader = ItemLoader(item=items.LeroyMerlinItem(), response=response)
        loader.add_xpath('name', '//h1[@class="header-2"]/text()')
        loader.add_xpath('images', '//picture[@slot="pictures"]//img[@alt="product image"]/@src')
        loader.add_xpath('params', '//div[@class="def-list__group"]')
        loader.add_value('link', response.url)
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('_id', '//span[@slot="article"]/@content')
        yield loader.load_item()


