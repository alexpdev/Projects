# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from .http import ScraleniumRequest, ScraleniumResponse
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


DRIVERS = {
    "chrome": webdriver.Chrome,
    "firefox": webdriver.Firefox,
    "remote": webdriver.Remote,
}


class ScraleniumSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.



    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScraleniumDownloaderMiddleware:

    @classmethod
    def from_crawler(cls, crawler):
        headless = crawler.settings.get('HEADLESS', True)
        executable = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE')
        name = crawler.settings.get('SELENIUM_DRIVER_NAME')
        timeout = crawler.settings.get('TIMEOUT')
        s = cls(headless, executable, name, timeout)
        crawler.signals.connect(s.spider_closed, signal=signals.spider_closed)
        return s

    def __init__(self, headless, executable, name, timeout):
        self.headless = headless
        self.executable = executable
        self.name = name
        self.timeout = timeout
        self._driver = None
        self.images = []


    @property
    def driver(self):
        if not self._driver:
            if not self.name:
                self.name = "chrome"
            driverclass = DRIVERS[self.name]
            if self.executable:
                self._driver = driverclass(self.executable)
            else:
                self._driver = driverclass()
        return self._driver


    def process_request(self, request, spider):
        if not isinstance(request, ScraleniumRequest):
            return None
        driver = self.driver
        # try:
        #     user_agent = request.headers['User-Agent'].decode('utf-8')
        #     driver.execute_cdp_cmd(
        #         'Network.setUserAgentOverride',{"userAgent": user_agent}
        #     )
        # except AttributeError:
        #     pass
        driver.get(request.url)
        for name, value in request.cookies.items():
            driver.add_cookie({
                'name': name,
                'value': value
            })
        if request.pause:
            time.sleep(request.pause)
        if request.screenshot:
            if request.screenshot_count:
                self._screenshots(request.screenshot_count,
                                  request.screenshot_duration)
            else:
                self._screenshot()
        request.images = self.images
        if request.script:
            driver.execute_script(request.script)
        body = driver.page_source
        response = ScraleniumResponse(
            driver,
            driver.current_url,
            request=request,
            body=body.encode('utf-8'),
            encoding='utf-8',
        )
        return response

    def _screenshot(self):
        image = self.driver.get_screenshot_as_png()
        self.images.append(image)

    def _screenshots(self, qty, duration):
        for _ in range(qty-1):
            self._screenshot()
            time.sleep(duration)
        self._screenshot()

    def spider_closed(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        self.driver.quit()
