# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from pprint import pprint
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ReviewsSpider(scrapy.Spider):
    name = "tripadvisor-spider"

    # set custom settings
    custom_settings = {
        'FEED_URI': 'file:///C:/Users/acfelk/Documents/IIT_Files/final year/FYP/fyp_workfiles/final_project/backend/drops/%(hotel_name)s.csv',
        'FEED_FORMAT': 'csv',
    }

    allowed_domains = ["tripadvisor.com"]
    # start_urls = (
    #     'https://www.tripadvisor.com/Attraction_Review-g304141-d4782530-Reviews-Sigiriya_World_Heritage_Site-Sigiriya_Central_Province.html',
    # )

    def __init__(self, *args, **kwargs):
        self.hotel_name = kwargs.get('hotel_name')
        self.start_urls = [kwargs.get('start_url')]
        super(ReviewsSpider, self).__init__(*args, **kwargs)
        self.review_count = kwargs.get('review_count')


    def parse(self, response):
        allreviewsinpage = response.xpath('.//*[@class="hotels-review-list-parts-SingleReview__reviewContainer--d54T4"]')

        for eachreview in allreviewsinpage:

            more = response.xpath("//p[@class='partial_entry']/span")

            for x in range(0, len(more)):
                try:
                    more[x].click()
                except:
                    pass

            for idx,review in enumerate(response.css('div.review-container')):
                yield {
                    'text': review.css('p.partial_entry::text').extract_first(),
                }

            next_page = response.xpath('//div[@class="pageNumbers"]/a[contains(@class,"current")]/following-sibling::a[1]').extract_first()

            if next_page is not None and (self.revCount <= self.review_count):
                next_page_url = response.urljoin(next_page)
                yield scrapy.Request(next_page_url, callback=self.parse_review)

    def parse(self, response):
        page_count = 0
        self.driver.get(response.url)
        next_page = self.driver.find_element_by_xpath('//div[@class="pageNumbers"]/a[contains(@class,"current")]/following-sibling::a[1]')
        pages = int(self.review_count) / 10
        while page_count < pages:
            if next_page is None:
                break

            page_count = page_count + 1
            more = self.driver.find_elements_by_xpath("//p[@class='partial_entry']/span")
            for x in range(0,len(more)):
                try:
                    more[x].click()
                except:
                    pass
            try:
                wait = WebDriverWait(self.driver, 20)
                element = wait.until(EC.text_to_be_present_in_element((By.XPATH,"//div[@class='entry']/span"),"Show less"))
            finally:
                res = Selector(text=self.driver.page_source)

            for idx,review in enumerate(res.css('div.review-container')):
                yield {
                    'text': review.css('p.partial_entry::text').extract_first(),
                }

            next_page.click()
            try:
                wait2= WebDriverWait(self.driver, 20)
                element2 = wait2.until(wait_for_load(self.driver.find_element_by_xpath("//div[@class='review-container']").text))
            except:
                pass
            try:
                next_page = self.driver.find_element_by_xpath('//div[@class="pageNumbers"]/a[contains(@class,"current")]/following-sibling::a[1]')
            except:
                pass
        self.driver.close()




# USE BELOW COMMAND TO RUN
# scrapy runspider tripadvisor_scrap.py -a review_count=100 -a start_url="https://www.tripadvisor.com/Hotel_Review-g293962-d2038179-Reviews-Galle_Face_Hotel_Colombo-Colombo_Western_Province.html" -o reviews.csv
