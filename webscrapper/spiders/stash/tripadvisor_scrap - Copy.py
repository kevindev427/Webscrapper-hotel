# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from pprint import pprint
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class wait_for_load(object):
    def __init__(self,old):
        self.old = old
    def __call__(self, driver):
        element = driver.find_element_by_xpath("//div[@class='review-container']")   # Finding the referenced element
        if self.old != element.text:
            return element
        else:
            return False

class ReviewsSpider(scrapy.Spider):
    name = "reviews"
    allowed_domains = ["tripadvisor.com"]
    # start_urls = (
    #     'https://www.tripadvisor.com/Attraction_Review-g304141-d4782530-Reviews-Sigiriya_World_Heritage_Site-Sigiriya_Central_Province.html',
    # )

    def __init__(self, *args, **kwargs):
        self.start_urls = [kwargs.get('start_url')]
        self.review_count = kwargs.get('review_count')
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Chrome()

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
# scrapy runspider tripadvisor_scrap.py -a review_count=100 -a start_url="https://www.tripadvisor.com/Attraction_Review-g304141-d4782530-Reviews-Sigiriya_World_Heritage_Site-Sigiriya_Central_Province.html" -o reviews.csv
