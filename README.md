# Scralenium

<!--- These are examples. See https://shields.io for others or to customize this set of shields. You might want to include dependencies, project status and licence info here --->

![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/scralenium?color=orange)
![GitHub License](https://img.shields.io/github/license/alexpdev/scralenium?color=red&logo=apache)
![PyPI - Downloads](https://img.shields.io/pypi/dm/scralenium?color=brown)
![GitHub Last Commit](https://badgen.net/github/last-commit/alexpdev/scralenium?color=blue&icon=github)
[![CI](https://github.com/alexpdev/scralenium/actions/workflows/windows.yml/badge.svg?branch=master&event=push)](https://github.com/alexpdev/scralenium/actions/workflows/windows.yml)
[![CI](https://github.com/alexpdev/scralenium/actions/workflows/mac.yml/badge.svg?branch=master&event=push)](https://github.com/alexpdev/scralenium/actions/workflows/mac.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/alexpdev/scralenium)
[![codecov](https://codecov.io/gh/alexpdev/scralenium/branch/main/graph/badge.svg?token=jpj9Rgriqi)](https://codecov.io/gh/alexpdev/scralenium)

Project name is a `scralenium` that allows _use selenium webdriver with scrapy_ to do scrape web data from dynamic web pages.  The name is actually really clever, if you didn't notice it is `scrapy` + `selenium` = `scralenium`.  Genius right? :)

## Prerequisites

Before you begin, ensure you have met the following requirements:

-   You have installed the latest version of `python 3`
-   You are familiar with the scrapy framework
-   You are familiar with selenium
-   You have a webdriver installed/available

Requirements:

-   scrapy
-   selenium

## Installing

To install `scralenium`, follow these steps:

```bash
git clone https://github.com/alexpdev/scralenium.git
cd scralenium
pip install .
```

From PyPi

```bash
pip install scralenium
```

## License

This project uses the following license: [Apache 2.0](./LICENSE).

## Usage

Using `scralenium` is really simple.

In your scrappy settings set the `SELENIUM_DRIVER_NAME` and
`SELENIUM_DRIVER_EXECUTABLE` fields. **`scralenium`** currently supports
chrome SELENIUM_DRIVER_NAME field. If the webdriver executable is already
on `path` then it can be omitted. You also need to enable the
`ScraleniumDownloaderMiddleware` in the `DOWNLOADER_MIDDLEWARES` feed.

```python
from shutil import which
SELENIUM_DRIVER_EXECUTABLE = which("chromedriver")
SELENIUM_DRIVER_NAME = "chrome"
DOWNLOADER_MIDDLEWARES = {
    "scralenium.ScraleniumDownloaderMiddleware" : 950
}
```

Once you have added the settings to the `settings.py` file or in the 
spider's `custom_settings` attribute all that is needed is to use 
`ScraleniumRequest` when yielding from the `start_requests` method or
from your parse callback methods. The `pause` argument can be used to set
the webdrivers implicit wait value.  And the `response` argument in the 
parse callback methods gives you full access to the normal scrapy response 
as well as all the features of the webdriver.

```python
import scrapy
from scralenium import ScraleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class MySpider(scrapy.Spider):
    """Example of using scrapy.Spider with ScraleniumRequest"""
    ...
     
    def start_requests(self):
        for url in self.start_urls:
            yield ScreleniumRequest(url, callback=self.parse, pause=4)
    
    def parse(self, response):
        html = response.text
        title = response.xpath("//title/text()").get()
        element = response.find_element(By.ID, "submit-button")
        element.send_keys(Keys.Return)
        next_page = response.xpath("//a[@class='next-page-link']/@href").get()
        next_url = response.urljoin(next_page)
        yield ScraleniumRequest(next_url, callback=self.parse, pause=4)
        yield {"title": title}
```

I have added some additional features but am behind on documenting them.

## TODO

[x] add features  
[] document them
