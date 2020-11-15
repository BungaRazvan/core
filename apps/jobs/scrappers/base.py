from typing import List, Union

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class ScrapperBase:
    """Base class for a selenium scraper."""

    options = None

    def __init__(self, browser: str, arguments: Union[List[str], None] = None):
        """Initialise a scrapper instance.

        :param browser: Type of browser
        :param arguments: selenium arguments
        """

        if arguments is not None:
            self.options = Options()

            for arg in arguments:
                self.options.add_argument(arg)

        if browser == "chrome":
            self.driver = webdriver.Chrome(options=self.options)

        elif browser == "firefox":
            self.driver = webdriver.Firefox(options=self.options)

        else:
            raise Exception(f"Unknown browser {browser}")

    def load_page(self, url: str):
        """Load one page.

        :param url: page address
        """

        self.driver.get(url)

    def scrape_pages(self, urls: List[str]):
        """Scrape multiple pages.

        :param urls: pages address
        """

        for url in urls:
            self.load_page(url=url)
            self.scrape_page()

    def scrape_page(self) -> NotImplementedError:
        """Scrape a page to be implemented by each class."""

        raise NotImplementedError
