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

    def parse_quantity(self, item):
        quantity = float(item.get('content_quantity'))
        if quantity == 0:
            return 1
        else:
            return quantity

    def parse(self, response):
        data = json.loads(response.body)
        for item in data.get('results', []):
            price = float(self.parse_price(item))
            quantity = self.parse_quantity(item)
            img = item.get('images')[0].get('categoryimage')
            skuid = item.get('skuid')[0]
            yield {
                'img': img,
                'img_url': 'https://ecoop.ee/%s' % img,
                'price': price,
                'unitprice': price / quantity,
                'product': item.get('name'),
                'id': item.get('gtin')[0],
                'url': 'https://ecoop.ee/api/v1/products?skuid=%s' % skuid ,
            }
        if data['next']:
            next_page = data['next']
            yield scrapy.Request(self.base_url % next_page)
