import scrapy

class SelverSpider(scrapy.Spider):
    name = 'selver'

    start_urls = ['https://www.selver.ee/']

    def parse(self, response):
        for href in response.css('nav ul li a::attr(href)'):
            yield response.follow(href, self.parse_products)

    def parse_price(self, selector):
        try:
            return float(selector.css('.left .price::text').re_first(r'[\d.,]+').replace(",", "."))
        except:
            return ''

    def parse_unitprice(self, selector):
        try:
            return float(selector.css('.left .unit-price::text').re_first(r'[\d.,]+').replace(",", "."))
        except:
            return ''

    def parse_products(self, response):
        for quote in response.css('#products-grid li'):
            yield {
                'img': quote.css('a > img::attr("src")').extract_first(),
                'img_url': quote.css('a > img::attr("src")').extract_first(),
                'price': self.parse_price(quote),
                'unitprice': self.parse_unitprice(quote),
                'product': quote.css('h5.product-name a::text').extract_first(),
                'id': quote.css('::attr("data-product-id")').extract_first(),
                'url': quote.css('a::attr("href")').extract_first(),
            }
        next_page = response.css('ol.pagination li a.next::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse_products)
