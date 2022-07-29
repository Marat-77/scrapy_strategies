# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Join


def preprocess_digits(value):
    if value:
        value = value.replace(' ', '')
        try:
            value = int(value)
        except:
            pass
    return value


def preprocess_description(value):
    value = value.replace('\xad', '')
    value = value.replace('\n', '')
    value = value.replace('\ufeff', '')
    value = value.replace('\xa0', '')
    value = value.strip()
    return value


class StrategiesparserItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    strategy_link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    author_link = scrapy.Field(output_processor=TakeFirst())
    author_name = scrapy.Field(output_processor=TakeFirst())
    subscribers = scrapy.Field(input_processor=MapCompose(preprocess_digits),
                               output_processor=TakeFirst())
    year_profit = scrapy.Field(input_processor=MapCompose(preprocess_digits))
    year_profit_measure = scrapy.Field()
    min_deposit = scrapy.Field(input_processor=MapCompose(preprocess_digits))
    min_deposit_currency = scrapy.Field()
    max_loss = scrapy.Field(input_processor=MapCompose(preprocess_digits))
    max_loss_measure = scrapy.Field()
    risk_level = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(input_processor=MapCompose(preprocess_description),
                               output_processor=Join())
