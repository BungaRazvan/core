from typing import Union, Dict

import csv
import datetime
import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver

from apps.jobs.scrappers.base import ScrapperBase


class AmazonScrapper(ScrapperBase):

    base_url = "https://www.amazon.co.uk/"

    HEADER = [
        "Product Name",
        "Product Price",
        "Product Deal",
        "Product RRP",
        "Product Availability",
        "Date",
    ]

    def __init__(self):
        super().__init__(browser="chrome", provider="amazon")

    def store_data(self, data: dict) -> None:
        self.write_to_csv(header=self.HEADER, filename="test.csv", data=data)

    def scrape_page(self):
        data = self.scrape_product(self.driver)

        self.store_data(data)

    @staticmethod
    def scrape_product(driver: WebDriver) -> Dict:
        """Scrape a product page.

        :param driver: selenium web driver
        """

        price = None
        deal_price = None
        rrp = None

        product_title = driver.find_element_by_id("productTitle").text
        availability = driver.find_element_by_id("availability").text

        try:
            price = driver.find_element_by_id("priceblock_ourprice").text
        except NoSuchElementException:
            deal_price = driver.find_element_by_id("priceblock_dealprice").text
            rrp = driver.find_element_by_class_name("priceBlockStrikePriceString").text

        return {
            "Product Name": product_title,
            "Product Price": price,
            "Product Deal": deal_price,
            "Product RRP": rrp,
            "Product Availability": availability,
            "Date": datetime.datetime.now(),
        }

    @staticmethod
    def write_to_csv(header: Union[list, tuple], filename: str, data: Dict[str, str]):
        if os.path.exists(filename):

            with open(f"{filename}", "a+") as file:
                writer = csv.DictWriter(file, fieldnames=header, delimiter=";")

                writer.writerow(data)

        else:
            with open(f"{filename}", "w") as file:
                writer = csv.DictWriter(file, fieldnames=header, delimiter=";")

                writer.writeheader()
                writer.writerow(data)


AmazonScrapper().scrape_pages([AmazonScrapper.urls])
