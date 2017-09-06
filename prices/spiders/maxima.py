import scrapy

class MaximaSpider(scrapy.Spider):
    name = 'maxima'

    start_urls = ['https://www.e-maxima.ee/Products/sook-ja-jook.aspx']

    def parse(self, response):
        # follow links to author pages
        for href in response.css('#submenu a::attr(href)'):
            yield response.follow(href, self.parse_products)

    def parse_products(self, response):
        for quote in response.css('tr'):
            yield {
                'price': quote.css('tr td:nth-child(3) strong::text').extract_first(),
                'product': quote.css('tr td:nth-child(2) h3 a:first-child::text').extract_first(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)