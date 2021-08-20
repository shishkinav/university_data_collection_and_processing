from abc import ABC, abstractmethod
import hashlib
from booklife import items


class BaseConverter(ABC):
    @abstractmethod
    def prepare_data(self, item) -> dict:
        """
        Обязательный метод, отвечающий за подготовку Item
            перед сохранением в БД
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
