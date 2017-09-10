# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PricesItem(scrapy.Item):
    img = scrapy.Field()
    price = scrapy.Field()
    unitprice = scrapy.Field()
    product = scrapy.Field()
