import scrapy
from scrapy.selector import Selector

class GBRspider(scrapy.Spider):
    name = 'epiroc'

    custom_settings = {
        "CONCURRENT_REQUESTS": 3,
    }


    def start_requests(self):
        for i in range(1, 300):
            yield scrapy.Request(f"https://epiroc-m2-stg.vaimo.net/en/our-products?p={i}&vajax_blocks=product_list", dont_filter=True)

    def parse(self, response):
        for block in response.json()["blocks"]:
            if "product-list-item-link" in block["html"]:
                selector = Selector(text=block["html"])
                for item in selector.xpath("//a[@class='product-list-item-link']"):
                    link = item.xpath("./@href").get()
                    yield scrapy.Request(link, callback=self.parse_product)

    def parse_product(self, response):
        part_number = response.xpath("//span[@class='product-info__sku--part-number']/text()").get()
        price = response.xpath("//span[@data-price-amount]/@data-price-amount").get()
        name = response.xpath("//div[@class='product-info__name']/h1/text()").get()
        category = response.xpath("//a[@class='product-info__categories']/text()").get()
        item = dict(part_number=part_number, price=price, name=name, category=category)
        for row in response.xpath("//table[@id='product-attribute-specs-table']//tr"):
            label = row.xpath(".//th/text()").get().strip()
            value = row.xpath(".//td/text()").get().strip()
            item[label] = value
        yield item
