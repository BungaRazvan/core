from apps.jobs.scrappers.base import ScrapperBase


class AmazonScrapper(ScrapperBase):

    base_url = "https://www.amazon.co.uk/"

    urls = "https://www.amazon.co.uk/dp/B08FT71HH5/?coliid=IJ50N6BA5O1LZ&colid=OXRN1JKMZVV9&ref_=lv_ov_lig_dp_it&th=1"

    def scrape_page(self):
        """Scrape a page."""

        product_title = self.driver.find_element_by_id("productTitle")
        availability = self.driver.find_element_by_id("availability")
        price = self.driver.find_element_by_id("priceblock_ourprice")

        print(price, product_title, availability)


AmazonScrapper(browser="chrome").scrape_pages([AmazonScrapper.urls])
