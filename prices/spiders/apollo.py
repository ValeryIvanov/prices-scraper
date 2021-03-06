# -*- coding: utf-8 -*-
import scrapy
import json

class ApolloSpider(scrapy.Spider):
    name = 'apollo'

    start_urls = ['https://www.apollo.ee/raamatud/eestikeelsed-raamatud/lastekirjandus']

    def parse(self, response):
        for products_grid in response.css('.category-products .products-grid'):
            for item in products_grid.css('.item'):
                soldout = item.css('.souldout')
                product_name = item.css('.product-name a::text')
                if soldout:
                    self.logger.info('Skipping %s, since sold out', product_name)
                    continue
                product_url = item.css('.image-wrapper a::attr("href")').extract_first()
                self.logger.info('Product %s not sold out, processing', product_name)
                yield scrapy.Request(product_url, callback=self.parse_product)
        next_page = response.css('.pager .right a::attr("href")').extract_first()
        if next_page is not None:
            self.logger.info('Found next page %s', next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            self.logger.info('No more pages left, exiting')

    def parse_price(self, selector):
        try:
            return float(selector.css('.price::text').re_first(r'[\d.,]+').replace(",", "."))
        except:
            self.logger.info('Failed to parse price')
            return ''

    def parse_id(self, selector):
        try:
            return selector.css('tr td a::attr("href")').extract_first().split('?')[1]
        except:
            return ''

    def parse_attributes(self, selector):
        try:
            attributes = list(map(lambda li: {li.css('*::text')[1].extract().strip(): li.css('*::text')[2].extract().strip()}, selector.css('#product-attribute-specs-table li')))
            a = [{i:j for x in attributes for i,j in x.items()}]
            return a[0]
        except:
            self.logger.info('Failed to parse price')
            return {}

    def parse_pages(self, attributes):
        try:
            return int(attributes[u'Lehek\xfclgi:'])
        except:
            return 0

    def parse_product(self, response):
        attributes = self.parse_attributes(response)
        yield {
            'id': response.css('.link-wishlist::attr("data-wishlist")').extract_first(),
            'product': response.css('.product-name h1::text').extract_first(),
            'img_url': response.css('.product-page-img img::attr("src")').extract_first(),
            'url': response.url,
            'price': self.parse_price(response),
            'attributes': attributes,
            'pages': self.parse_pages(attributes),
            'description': response.css('#description::text').extract_first()
        }
