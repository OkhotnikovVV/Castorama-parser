import os
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from src.spiders.castorama import CastoramaSpider

os.environ["SCRAPY_SETTINGS_MODULE"] = "src.settings"


if __name__ == '__main__':
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(CastoramaSpider, query='радиатор')

    reactor.run()
