from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from booklife import settings
from booklife.spiders.labirintru import LabirintruSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LabirintruSpider)

    process.start()

"""
Выдержка из 540 спарсенных данных
[
  {
    "_id": "5de4f485503dfcdeb313aebd99b4679636bce74c",
    "authors": ["Митчелл Сэнди"],
    "link": "https://www.labirint.ru/books/663872/",
    "name": "Защитник Империума",
    "price_new": "1217",
    "price_old": "1739",
    "rate": 10
  },
  {
    "_id": "cb46255f00e8dc2854930902da2f2b2b6673c9f0",
    "authors": ["Валентеева Ольга Александровна"],
    "link": "https://www.labirint.ru/books/813945/",
    "name": "Врата пустоты. Зеркальный страж",
    "price_new": "347",
    "price_old": "495",
    "rate": 9.12
  },
  {
    "_id": "b726e0217f9e653b61a38f20621a98c897821d1a",
    "authors": ["Кузнецова Дарья Андреевна"],
    "link": "https://www.labirint.ru/books/812145/",
    "name": "Цена ошибки некроманта",
    "price_new": "347",
    "price_old": "495",
    "rate": 9
  },
  {
    "_id": "e33f4cda97ace314960ad0a94d80a4985f322aec",
    "authors": ["Хейли Гай", "Райт Крис", "Макнилл Грэм", "Харрисон Рэйчел"],
    "link": "https://www.labirint.ru/books/811347/",
    "name": "Воители и вожди",
    "price_new": "957",
    "price_old": "1367",
    "rate": 0
  }
]
"""