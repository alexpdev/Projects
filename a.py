import sys
from scrapy.cmdline import execute

sys.argv = ["scrapy", "crawl", "odds", "-o", "a.json"]

execute()
