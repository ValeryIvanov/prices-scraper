from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from prices.spiders.coop import CoopSpider
from prices.spiders.maxima import MaximaSpider
from prices.spiders.selver import SelverSpider
from prices.spiders.prisma import PrismaSpider

process = CrawlerProcess(get_project_settings())

process.crawl(CoopSpider)
process.crawl(MaximaSpider)
process.crawl(SelverSpider)
process.crawl(PrismaSpider)

process.start() # the script will block here until all crawling jobs are finished
