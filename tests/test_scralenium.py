"""Testing module for scralenium."""

import pytest
from scrapy import Request

from scralenium import middlewares
from scralenium.__version__ import __version__
from scralenium.http import ScraleniumRequest, ScraleniumResponse
from scralenium.middlewares import ScraleniumDownloaderMiddleware


def test_version():
    """Test scralenium version sym version"""
    assert isinstance(__version__, str)
    assert __version__.count(".") == 2


class Spider:
    """Dummy Spider."""

    name = "test"

    class logger:
        """Dummy logger."""

        @staticmethod
        def info(msg):
            """Do nothing with msg."""
            assert msg


class Driver:
    """Dummy Driver."""

    page_source = "<html><body><p>Nothing</p></body></html>"
    current_url = "https://some_url"

    def __init__(self, executable=None):
        """Construct dummy Driver."""
        self.executable = executable

    def execute_cdp_cmd(self, thing1, thing2):
        """Do Nothing with thing1 and thing2."""
        self.thing1 = thing1
        self.thing2 = thing2

    def get(self, url):
        """Do nothing with url."""
        self.url = url

    def implicitly_wait(self, value):
        """Wait till value is 0."""
        while value > 0:
            value -= 1
        self.value = value

    def execute_script(self, script):
        """Execute script."""
        self.script = script

    def get_screenshot_as_png(self):
        """Return a screenshot"""
        self.shot = [0, 0, 0]
        return self.shot

    def add_cookie(self, mapp):
        """Add cookie to cookies."""
        self.mapp = mapp

    def quit(self):
        """Do nothing."""
        self.closed = True


middlewares.DRIVERS = {"chrome": Driver}


class Signal:
    """Signal class."""

    @staticmethod
    def connect(thing1, signal=None):
        """Do nothing."""


class DummyCrawler:
    """Crawler class dummy."""

    settings = {
        "SELENIUM_DRIVER_EXECUTABLE": None,
        "SELENIUM_DRIVER_NAME": "chrome",
    }
    signals = Signal()


def test_request():
    """Test scraleniumrequest object."""
    url = "https://some.url.com"
    pause = 12
    request = ScraleniumRequest(
        url, pause=pause, callback=lambda x: str(x) + "l"
    )
    assert request.pause == pause
    assert request.url == url


@pytest.fixture
def req():
    """Return a ScraleniumRequest"""
    return ScraleniumRequest(
        "https://some.url.com", pause=10, callback=lambda x: str(x) + "s"
    )


@pytest.fixture
def req2():
    """Return regular scrapy request."""
    return Request("https://some.url.com", callback=lambda x: str(x) + "s")


def test_response(req):
    """Test ScraleniumResponse object."""
    dummy = {"unittest": "test_response"}
    images = []
    body = b"<html><body><h1>Test</h1></body></html>"
    resp = ScraleniumResponse(
        dummy, req.url, request=req, images=images, body=body, encoding="utf8"
    )
    assert resp.images == images
    assert resp.xpath("//h1/text()").get() == "Test"
    assert resp.get("unittest") == dummy["unittest"]


def test_response_error(req):
    """Test ScraleniumResponse object errors."""
    dummy = {"unittest": "fail"}
    images = []
    body = b"<html><body><h1>Fail</h1></body></html>"
    resp = ScraleniumResponse(
        dummy, req.url, request=req, images=images, body=body, encoding="utf8"
    )
    assert resp.images == images
    assert resp.xpath("//h1/text()").get() == "Fail"
    try:
        assert resp.over("")
    except AttributeError:
        assert True


@pytest.mark.parametrize("name", [True, False])
@pytest.mark.parametrize("executable", [True, False])
@pytest.mark.parametrize("close", [True, False])
@pytest.mark.parametrize("driver", [True, False])
@pytest.mark.parametrize("script", ["script", None])
@pytest.mark.parametrize("cookies", [("name", "value"), None])
@pytest.mark.parametrize("ua", ["scrapy", "mozilla", None])
@pytest.mark.parametrize("screenshot", [None, (None, None), (3, 0.03)])
def test_process_request(
    req, ua, cookies, script, screenshot, driver, name, executable, close
):
    """Test the process_request method."""
    crawler = DummyCrawler()
    instance = ScraleniumDownloaderMiddleware.from_crawler(crawler)
    if name:
        instance.name = None
    if executable:
        instance.executable = "path"
    if driver:
        instance._driver = Driver()
    spider = Spider()
    if cookies:
        req.cookies[cookies[0]] = cookies[1]
    if ua:
        req.headers["User-Agent"] = ua
    if script:
        req.script = script
    if screenshot:
        req.screenshot = True
        req.screenshot_count = screenshot[0]
        req.screenshot_duration = screenshot[1]
    resp = instance.process_request(req, spider)
    assert isinstance(resp, ScraleniumResponse)
    if close:
        instance.spider_closed(spider)


def test_process_request2(req2):
    """Test the process_request method with regular request."""
    crawler = DummyCrawler()
    instance = ScraleniumDownloaderMiddleware.from_crawler(crawler)
    spider = Spider()
    resp = instance.process_request(req2, spider)
    assert resp is None
