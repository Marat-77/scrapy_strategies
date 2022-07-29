import scrapy
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import selenium

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
        # print(response.status)
        pages_buttons = response.xpath(
            '//nav/ul/li/button/text()'
        ).getall()
        # print(len(pages_buttons))  # 10
        # print(pages_buttons[-1])  # <Selector xpath='//nav/ul/li/button/text()' data='56'>
        # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # last_page = pages_buttons[-1]
        # page_number = 1
        # while str(page_number) != last_page:
        #     page_number += 1
        #     next_url = f'https://www.comon.ru/strategies/' \
        #                f'?LifeSpan=Undefined&page={page_number}'
        #     yield SeleniumRequest(url=next_url)
        # # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # список ссылок на страницы стратегий:
        strategies_links = response.xpath(
            '//div[contains(@class, "MuiCard-root")]/a/@href'
        ).getall()
        # print(len(strategies_links))
        # print()
        for strategy_link in strategies_links:
            print(strategy_link)
            # https://www.comon.ru/strategies/11537
            strategy_link = f'https://www.comon.ru{strategy_link}'
            print(strategy_link)
            yield SeleniumRequest(url=strategy_link,
                                  callback=self.parse_strategy_page)

    def parse_strategy_page(self, response: HtmlResponse):
        print(response)
        # print()
        # название стратегии:
        title = response.xpath('//h1/text()').get()
        # ссылка на автора стратегии:
        author_link = response.xpath('//div[@class="MuiCardHeader-content"]/span/a/@href').get()
        # автор стратегии:
        author_name = response.xpath('//div[@class="MuiCardHeader-content"]/span/a/span/text()').get()
        # количество подписчиков:
        subscribers = response.xpath('//div[@class="MuiCardHeader-content"]/p/text()[2]').get()
        # доходность за год:
        year_profit = response.xpath('//p[contains(text(),"Доходность за год")]/following-sibling::p/span/text()').getall()
        # [' -34', ' ', '%']
        # минимальная сумма:
        min_deposit = response.xpath('//p[contains(text(),"Минимальная сумма")]/following-sibling::p/span/text()').getall()
        # ['35 000', ' ', '₽']
        # максимальная просадка:
        max_loss = response.xpath('//p[contains(text(),"Максимальная просадка")]/following-sibling::p/span/text()').getall()
        # [' -49', ' ', '%']
        # риск:
        risk_level = response.xpath('//p[contains(text(),"Риск")]/following-sibling::p/text()').get()
        # 'Консервативный'
        # описание:
        description = response.xpath('//h6[contains(text(), "Описание")]/following-sibling::div//text()').getall()
        print()
        # - много текста :)
        # div_svg = response.xpath('//div[@class="recharts-wrapper"]').get()
        # график доходности:
        # chart_svg = response.xpath('//div[@class="recharts-wrapper"]/*[local-name()="svg"]').get()
        chart_svg = (By.XPATH, '//div[@class="recharts-wrapper"]/*[local-name()="svg"]')
        chart_svg = SeleniumRequest(
            url=response.url,
            wait_time=10,
            wait_until=EC.visibility_of_element_located(chart_svg)
        )
        print()
        # кнопка "ПОКАЗАТЕЛИ":
        # button_indications = response.xpath(('//button/span[contains(text(), "Показатели")]/parent::button')).get()
        button_indications = (
            By.XPATH,
            '//button/span[contains(text(), "Показатели")]/parent::button'
        )
        button_indications = SeleniumRequest(
            url=response.url,
            wait_time=10,
            wait_until=EC.element_to_be_clickable(button_indications)
        )
        # button_indications = ActionChains()
        button_indications.click()
        print()

