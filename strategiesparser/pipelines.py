# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


import pymongo
from pymongo.errors import DuplicateKeyError


class StrategiesparserPipeline:
    """
    Конвейер сохраняет полученную информацию о товарах в базу данных MongoDB
    """

    def __init__(self, mongo_host, mongo_port, mongo_db, mongo_coll):
        """Инициализация конвейера с настройками MongoDB."""
        self.mongo_host = mongo_host
        self.mongo_port = mongo_port
        self.mongo_db = mongo_db
        self.mongo_coll = mongo_coll

    @classmethod
    def from_crawler(cls, crawler):
        """
        Метод класса устанавливает атрибуты для соединения с базой данных MongoDB
        из настроек (settings.py)
        """
        return cls(
            mongo_host=crawler.settings.get('MONGO_HOST'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "scraping"),
            mongo_coll=crawler.settings.get("MONGO_COLLECTION", "quotes"),
        )

    def open_spider(self, spider):
        """Соединение с базой данных MongoDB"""
        self.client = pymongo.MongoClient(self.mongo_host, self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.mongo_coll]

    def close_spider(self, spider):
        """Закрытие соединения с базой данных MongoDB"""
        self.client.close()

    def process_item(self, item, spider):
        item['author_link'] = self.process_author_link(item)

        item['max_loss_measure'] = item['max_loss'][-1]
        item['max_loss'] = item['max_loss'][0]

        item['min_deposit_currency'] = item['min_deposit'][-1]
        item['min_deposit'] = item['min_deposit'][0]

        item['year_profit_measure'] = item['year_profit'][-1]
        item['year_profit'] = item['year_profit'][0]

        try:
            self.collection.insert_one(item)
        except DuplicateKeyError:
            item_id = item['_id']
            print(f'Запись _id:{item_id} уже есть в базе данных')
        return item

    @staticmethod
    def process_author_link(item):
        prefix = item['strategy_link'].split('/strategies/')[0]
        return f"{prefix}{item['author_link']}"
