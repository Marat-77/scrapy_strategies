import scrapy
from scrapy.http import HtmlResponse


class ComonSpider(scrapy.Spider):
    name = 'comon'
    allowed_domains = ['comon.ru']
    start_urls = ['https://www.comon.ru/strategies/?page=1']

    def parse(self, response: HtmlResponse):
        print()
