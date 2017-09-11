import scrapy

class SelverSpider(scrapy.Spider):
    name = 'selver'

    start_urls = ['https://www.selver.ee/']

    def parse(self, response):
        for href in response.css('nav ul li a::attr(href)'):
            yield response.follow(href, self.parse_products)

    def parse_products(self, response):
        for quote in response.css('#products-grid li'):
            yield {
                'img': quote.css('a > img::attr("src")').extract_first(),
                'price': quote.css('.left .price::text').extract_first(),
                'unitprice': quote.css('.left .unit-price::text').extract_first(),
                'product': quote.css('h5.product-name a::text').extract_first(),
            }
        next_page = response.css('ol.pagination li a.next::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
