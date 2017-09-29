import scrapy
import json

class PrismaSpider(scrapy.Spider):
    name = 'prisma'

    start_urls = ['https://prismamarket.ee/products/selection']
    base_url = 'https://prismamarket.ee%s'

    def parse(self, response):
        has_more_links = response.css('.categories-shelf').extract_first()
        links = response.css('.category-shelf-item .transparent a::attr(href)').extract()
        if has_more_links is not None:
            self.logger.info('Found more links to visit on page %s', response.url)
            for href in links:
                self.logger.info('Visiting page to see if it has more links or products %s', self.base_url % href)
                yield scrapy.Request(self.base_url % href, callback=self.parse)
        else:
            self.logger.info('Found products on url %s', response.url)
            yield scrapy.Request(response.url, headers={'Accept': 'application/json','charset':'UTF-8'}, callback=self.parse_products, dont_filter=True)

    def parse_products(self, response):
        self.logger.info('Parse function called on %s', response.url)
        data = json.loads(response.body)
        for item in data.get('entries', []):
            self.logger.info('Found following item %s', item)
            img = item.get('image_guid')
            ean = item.get('ean')
            yield {
                'img': img,
                'img_url': 'https://s3-eu-west-1.amazonaws.com/balticsimages/images/180x220/%s.png' % img,
                'price': item.get('price'),
                'unitprice': item.get('comp_price'),
                'product': item.get('name'),
                'id': item.get('ean'),
                'url': 'https://prismamarket.ee/entry/%s' % ean,
            }
        if data.get('pagination', {})['next_url']:
            next_page = data.get('pagination', {})['next_url']
            self.logger.info('Next url will be %s', self.base_url % next_page)
            yield scrapy.Request(self.base_url % next_page, headers={'Accept': 'application/json','charset':'UTF-8'}, callback=self.parse_products)
