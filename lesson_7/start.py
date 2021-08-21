from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from booklife import settings
from booklife.spiders.lm import LmSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmSpider, target='розетки')
    process.start()

"""
[
  {
    "_id": "82303143",
    "images": [
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/82303143.jpg",
        "path": "82303143/82303143.jpg",
        "checksum": "5f625e8310e24c9c522afaf6c7e47b85",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/82303143_01.jpg",
        "path": "82303143/82303143_01.jpg",
        "checksum": "5f4e0821baec3079ba170720d33e9b3a",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/82303143_02.jpg",
        "path": "82303143/82303143_02.jpg",
        "checksum": "cde834d02e7c2da2619619902a857349",
        "status": "downloaded"
      }
    ],
    "link": "https://volgograd.leroymerlin.ru/product/rozetka-dvoynaya-vstraivaemaya-lexman-viktoriya-s-zazemleniem-82303143/",
    "name": "Розетка двойная встраиваемая Lexman Виктория с заземлением, цвет белый",
    "params": {
      "Страна производства": "Китай",
      "Гарантия (лет)": "2",
      "Тип продукта": "Розетка",
      "Тип монтажа": "Встраиваемый",
      "Марка": "LEXMAN",
      "Серия": "Виктория",
      "Цвет": "Белый",
      "Наличие заземления": "Да",
      "Степень защиты от пыли и воды (IP)": "IP20",
      "Защита от детей": "Нет",
      "С крышкой": "Нет",
      "Сила тока (А)": "16.0",
      "Основной материал": "Керамика",
      "Выходное напряжение (В)": "220",
      "Тип крепления": "На винтах",
      "Ширина (мм)": "11.75",
      "Высота (мм)": "8.1",
      "Глубина (мм)": "4.11"
    },
    "price": 258
  },
  {
    "_id": "17782037",
    "images": [
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/17782037.jpg",
        "path": "17782037/17782037.jpg",
        "checksum": "0520d25c8b698d9a7a79551acc7ac7cb",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/17782037_01.jpg",
        "path": "17782037/17782037_01.jpg",
        "checksum": "2a0ce04a6ade12d6d6667239d5162490",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/17782037_02.jpg",
        "path": "17782037/17782037_02.jpg",
        "checksum": "dea3c2f9604f299b996398e659f8781c",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/17782037_03.jpg",
        "path": "17782037/17782037_03.jpg",
        "checksum": "137c88eca6dab755bce33baeb78faa04",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/17782037_04.jpg",
        "path": "17782037/17782037_04.jpg",
        "checksum": "a41a5d3052cdbfdd37e0cab56adce432",
        "status": "downloaded"
      },
      {
        "url": "https://res.cloudinary.com/lmru/image/upload/f_auto,q_auto,w_1200,h_1200,c_pad,b_white,d_photoiscoming.png/LMCode/17782037_i.jpg",
        "path": "17782037/17782037_i.jpg",
        "checksum": "21e268e7669c3e54a18a9464f80fec32",
        "status": "downloaded"
      }
    ],
    "link": "https://volgograd.leroymerlin.ru/product/rozetka-vstraivaemaya-werkel-s-zazemleniem-17782037/",
    "name": "Розетка встраиваемая Werkel с заземлением, со шторками, цвет белый",
    "params": {
      "Страна производства": "Китай",
      "Гарантия (лет)": "1",
      "Тип продукта": "Розетка",
      "Тип монтажа": "Встраиваемый",
      "Марка": "WERKEL",
      "Цвет": "Белый",
      "Наличие заземления": "Да",
      "Степень защиты от пыли и воды (IP)": "IP20",
      "Защита от детей": "Да",
      "С крышкой": "Нет",
      "Сила тока (А)": "16.0",
      "Основной материал": "Поликарбонат",
      "Выходное напряжение (В)": "220",
      "Тип крепления": "На винтах",
      "Ширина (мм)": "70.0",
      "Высота (мм)": "70.0",
      "Глубина (мм)": "43.0"
    },
    "price": 302
  }
]
"""