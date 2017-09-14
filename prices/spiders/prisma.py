import scrapy
import json

class PrismaSpider(scrapy.Spider):
    name = 'prisma'

    start_urls = ['https://prismamarket.ee/products/selection']
    base_url = 'https://prismamarket.ee%s'

    def parse(self, response):
        for href in response.css('.category-shelf-item .transparent a::attr(href)').extract():
            next_page = response.urljoin(href)
            self.logger.info('Found url to visit %s', next_page)
            yield scrapy.Request(next_page, headers={'Accept': 'application/json','charset':'UTF-8'}, callback=self.parse_products)

    def parse_products(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.body)
        for item in data.get('entries', []):
            self.logger.info('Found following item %s', item)
            yield {
                'img': item.get('image_guid'),
                'price': item.get('price'),
                'unitprice': item.get('comp_price'),
                'product': item.get('name'),
            }
        if data.get('pagination', {})['next_url']:
            next_page = data.get('pagination', {})['next_url']
            self.logger.info('Next url will be %s', self.base_url % next_page)
            yield scrapy.Request(self.base_url % next_page, callback=self.parse_products)
