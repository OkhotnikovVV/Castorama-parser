import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from src.items import CastoramaParserItem


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    start_urls = ['http://castorama.ru/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f"https://www.castorama.ru/catalogsearch/result/?q={kwargs.get('query')}"]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@class="product-card__img-link"]')
        for link in links:
            yield response.follow(link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoramaParserItem(), response=response)
        loader.add_xpath('name', '//h1[contains(@class, "product-essential__name")]/text()')
        loader.add_xpath('price', '//span[contains(@class, "price")]/span/span/span/text()')
        loader.add_xpath('photos', '//img[contains(@class, "top-slide__img")]/@data-src')
        loader.add_value('url', response.url)
        yield loader.load_item()
