import scrapy
from scrapy.http import HtmlResponse

from strategiesparser.items import StrategiesparserItem
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class ComonSpider(scrapy.Spider):
    name = 'comon'
    allowed_domains = ['comon.ru']
    start_urls = ['https://www.comon.ru/strategies/?LifeSpan=Undefined&page=1']

    def start_requests(self):
        if not self.start_urls and hasattr(self, 'start_url'):
            raise AttributeError(
                "Crawling could not start: 'start_urls' not found "
                "or empty (but found 'start_url' attribute instead, "
                "did you miss an 's'?)")
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    def parse(self, response: HtmlResponse):
        print(response.status)
        pages_buttons = response.xpath(
            '//nav/ul/li/button/text()'
        ).getall()
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        last_page = pages_buttons[-1]
        page_number = 1
        while str(page_number) != last_page:
            page_number += 1
            next_url = f'https://www.comon.ru/strategies/' \
                       f'?LifeSpan=Undefined&page={page_number}'
            yield SeleniumRequest(url=next_url)
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # список ссылок на страницы стратегий:
        strategies_links = response.xpath(
            '//div[contains(@class, "MuiCard-root")]/a/@href'
        ).getall()
        for strategy_link in strategies_links:
            strategy_link = f'https://www.comon.ru{strategy_link}'
            any_div = (By.XPATH, '//div/div')
            yield SeleniumRequest(url=strategy_link,
                                  callback=self.parse_strategy_page,
                                  wait_time=10,
                                  wait_until=EC.visibility_of_element_located(any_div))

    def parse_strategy_page(self, response: HtmlResponse):
        loader = ItemLoader(
            item=StrategiesparserItem(),
            response=response
        )
        # id стратегии:
        loader.add_value('_id', response.url.split('https://www.comon.ru/strategies/')[-1])

        # ссылка на стратегию:
        loader.add_value('strategy_link', response.url)

        # название стратегии:
        loader.add_xpath('title', '//h1/text()')

        # ссылка на автора стратегии:
        loader.add_xpath(
            'author_link',
            '//div[@class="MuiCardHeader-content"]/span/a/@href'
        )

        # автор стратегии:
        loader.add_xpath(
            'author_name',
            '//div[@class="MuiCardHeader-content"]/span/a/span/text()'
        )

        # количество подписчиков:
        loader.add_xpath(
            'subscribers',
            '//div[@class="MuiCardHeader-content"]/p/text()[2]'
        )

        # доходность за год:
        loader.add_xpath(
            'year_profit',
            '//p[contains(text(),"Доходность за год")]/following-sibling::p/span/text()'
        )

        # минимальная сумма:
        loader.add_xpath(
            'min_deposit',
            '//p[contains(text(),"Минимальная сумма")]/following-sibling::p/span/text()'
        )

        # максимальная просадка:
        loader.add_xpath(
            'max_loss',
            '//p[contains(text(),"Максимальная просадка")]/following-sibling::p/span/text()'
        )

        # риск:
        loader.add_xpath(
            'risk_level',
            '//p[contains(text(),"Риск")]/following-sibling::p/text()'
        )

        # описание:
        loader.add_xpath(
            'description',
            '//h6[contains(text(), "Описание")]/following-sibling::div//text()'
        )

        yield loader.load_item()
