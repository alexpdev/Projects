import scrapy
from scralenium.http import ScraleniumRequest


class TestSpider(scrapy.Spider):
    name = 'test'
    allowed_domains = ['alternativeto.net']

    def start_requests(self):
        start_urls = ['https://alternativeto.net/platform/linux/?feature=command-line-interface&license=opensource&sort=likes']
        for url in start_urls:
            yield ScraleniumRequest(url, pause=185)

    def parse(self, response):
        text = response.xpath("//div[contains(@class,'AppListItem_appHeader')]//text()").getall()
        yield {"text": text}
