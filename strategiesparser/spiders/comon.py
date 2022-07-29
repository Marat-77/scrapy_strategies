import time

import scrapy
from scrapy.http import HtmlResponse
from scrapy.utils.project import get_project_settings

from strategiesparser.items import StrategiesparserItem
from scrapy.loader import ItemLoader
from scrapy_selenium import SeleniumRequest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
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
        print(response.status)
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
            # print(strategy_link)
            # https://www.comon.ru/strategies/11537
            strategy_link = f'https://www.comon.ru{strategy_link}'
            # print(strategy_link)
            # chart_svg = (By.XPATH, '//div[@class="recharts-wrapper"]/*[local-name()="svg"]')
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
        # print(response)
        # time.sleep(10)
        # https://www.comon.ru/strategies/17353
        # id_strategy = response.url.split('https://www.comon.ru/strategies/')[-1]
        # print(id_strategy)
        loader.add_value('_id', response.url.split('https://www.comon.ru/strategies/')[-1])

        # strategy_link
        loader.add_value('strategy_link', response.url)
        # print()

        # название стратегии:
        # title = response.xpath('//h1/text()').get()
        loader.add_xpath('title', '//h1/text()')

        # ссылка на автора стратегии:
        # author_link = response.xpath('//div[@class="MuiCardHeader-content"]/span/a/@href').get()
        loader.add_xpath('author_link', '//div[@class="MuiCardHeader-content"]/span/a/@href')

        # автор стратегии:
        # author_name = response.xpath('//div[@class="MuiCardHeader-content"]/span/a/span/text()').get()
        loader.add_xpath('author_name', '//div[@class="MuiCardHeader-content"]/span/a/span/text()')

        # количество подписчиков:
        # subscribers = response.xpath('//div[@class="MuiCardHeader-content"]/p/text()[2]').get()
        loader.add_xpath('subscribers', '//div[@class="MuiCardHeader-content"]/p/text()[2]')

        # доходность за год:
        # year_profit = response.xpath('//p[contains(text(),"Доходность за год")]/following-sibling::p/span/text()').getall()
        # [' -34', ' ', '%']
        loader.add_xpath('year_profit', '//p[contains(text(),"Доходность за год")]/following-sibling::p/span/text()')

        # минимальная сумма:
        # min_deposit = response.xpath('//p[contains(text(),"Минимальная сумма")]/following-sibling::p/span/text()').getall()
        loader.add_xpath('min_deposit', '//p[contains(text(),"Минимальная сумма")]/following-sibling::p/span/text()')
        # ['35 000', ' ', '₽']

        # максимальная просадка:
        # max_loss = response.xpath('//p[contains(text(),"Максимальная просадка")]/following-sibling::p/span/text()').getall()
        # [' -49', ' ', '%']
        loader.add_xpath('max_loss', '//p[contains(text(),"Максимальная просадка")]/following-sibling::p/span/text()')

        # риск:
        # risk_level = response.xpath('//p[contains(text(),"Риск")]/following-sibling::p/text()').get()
        # 'Консервативный'
        loader.add_xpath('risk_level', '//p[contains(text(),"Риск")]/following-sibling::p/text()')

        # # --------------------------------------------------------------------------------------- * * *
        # # описание:
        # description = response.xpath('//h6[contains(text(), "Описание")]/following-sibling::div//text()').getall()
        loader.add_xpath('description', '//h6[contains(text(), "Описание")]/following-sibling::div//text()')
        # # - много текста :)
        # # --------------------------------------------------------------------------------------- * * *

        # # # ---------------------------------------------------------------------------------------
        # # driver = response.request.meta['driver']
        # webdriver_setting = get_project_settings().get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        # s = Service(webdriver_setting)
        # driver = webdriver.Chrome(service=s)
        # driver.implicitly_wait(30)
        # wait = WebDriverWait(driver, 30)
        # driver.get(response.url)
        #
        # # set window position 0, 0
        # driver.set_window_position(0, 0)
        # # window size 1280 720
        # driver.set_window_size(1280, 900)
        #
        # # кнопка "ПОКАЗАТЕЛИ":
        # button_indications = (
        #     By.XPATH,
        #     '//button/span[contains(text(), "Показатели")]/parent::button'
        # )
        # button = wait.until(EC.element_to_be_clickable(button_indications))
        # button.click()
        #
        # # theme = WebDriverWait(driver, timeout=10).until(
        # #     EC.presence_of_element_located((By.CLASS_NAME, 'thread-subject'))).text
        # # //p[contains(text(),'Структура')]/following-sibling::div//span[text()]
        # structure = (
        #     By.XPATH,
        #     '//p[contains(text(),"Структура")]/following-sibling::div//span[text()]'
        # )
        # structure = wait.until(EC.presence_of_element_located(structure)).text
        #
        # # # //p[contains(text(), "Тариф автоследования")]
        # # check_tariff = '//p[contains(text(), "Тариф автоследования")]'
        # # wait.until(EC.visibility_of_element_located((By.XPATH, check_tariff)))
        # # check_tariff = response.xpath(check_tariff).get()
        # # if check_tariff:
        # #     print('Ok!')
        # # print()
        # # # ---------------------------------------------------------------------------------------
        yield loader.load_item()
