import json
import scrapy

class CoopSpider(scrapy.Spider):
    name = 'coop'
    base_url = 'https://ecoop.ee/api/v1/products?page=%s'
    start_urls = [base_url % 1]

    def parse_price(self, item):
        try:
            return item.get('campaigns')[0].get('discounts')[0].get('price')
        except:
            return item.get('sell_price')

    def parse(self, response):
        data = json.loads(response.body)
        for item in data.get('results', []):
            price = float(self.parse_price(item))
            yield {
                'img': item.get('images')[0].get('categoryimage'),
                'price': price,
                'unitprice': price / float(item.get('content_quantity')),
                'product': item.get('name'),
            }
        if data['next']:
            next_page = data['next']
            yield scrapy.Request(self.base_url % next_page)
