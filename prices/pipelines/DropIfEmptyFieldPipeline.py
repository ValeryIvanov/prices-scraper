# -*- coding: utf-8 -*-

from scrapy.exceptions import DropItem

class DropIfEmptyFieldPipeline(object):

    def process_item(self, item, spider):

        if item['price']:
            return item
        else:
            raise DropItem("Missing price in %s" % item)
