from scrapy import Request
from scrapy.http import TextResponse


class ScraleniumRequest(Request):

    def __init__(
        self,
        *args,
        pause=None,
        screenshot=None,
        screenshot_count=None,
        screenshot_duration=None,
        script=None,
        **kwargs):
        self.pause = pause
        self.screenshot = screenshot
        self.screenshot_count = screenshot_count
        self.screenshot_duration = screenshot_duration
        self.script = script
        super().__init__(*args, **kwargs)



class ScraleniumResponse(TextResponse):

    def __init__(self, driver, *args, **kwargs):
        self.__driver = driver
        super().__init__(*args, **kwargs)

    def __getattr__(self, attr):
        if hasattr(self.driver, attr):
            return getattr(self.driver, attr)

    @property
    def driver(self):
        return self.__driver
