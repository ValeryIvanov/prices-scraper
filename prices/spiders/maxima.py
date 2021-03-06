import scrapy

class MaximaSpider(scrapy.Spider):
    name = 'maxima'

    start_urls = [
        'https://www.e-maxima.ee/Products/sook-ja-jook.aspx',
        'https://www.e-maxima.ee/Products/Majapidamistarbed.aspx',
        'https://www.e-maxima.ee/Products/Lastele.aspx',
        'https://www.e-maxima.ee/Products/Tervis-ja-ilu.aspx',
        'https://www.e-maxima.ee/Products/Puhkus-ja-lemmikloomad.aspx'
    ]

    def parse(self, response):
        for href in response.css('#submenu a::attr(href)'):
            yield response.follow(href, self.parse_products)

    def parse_price(self, selector):
        try:
            return float(selector.css('tr td:nth-child(3) strong::text').re_first(r'[\d.,]+').replace(",", "."))
        except:
            return ''

    def parse_unitprice(self, selector):
        try:
            return float(selector.css('tr td:nth-child(3) p::text')[1].re_first(r'[\d.,]+').replace(",", "."))
        except:
            return ''
    
    def parse_id(self, selector):
        try:
            return selector.css('tr td a::attr("href")').extract_first().split('?')[1]
        except:
            return ''

    def parse_img(self, selector):
        try:
            return selector.css('tr td.img img::attr("src")').extract_first()
        except:
            return ''

    def parse_products(self, response):
        for quote in response.css('tr'):
            img = self.parse_img(quote)
            yield {
                'img': img,
                'img_url': 'https://www.e-maxima.ee/%s' % img,
                'price': self.parse_price(quote),
                'unitprice': self.parse_unitprice(quote),
                'product': quote.css('tr td:nth-child(2) h3 a:first-child::text').extract_first(),
                'id': self.parse_id(quote),
                'url': quote.css('tr td a::attr("href")').extract_first(),
            }
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
