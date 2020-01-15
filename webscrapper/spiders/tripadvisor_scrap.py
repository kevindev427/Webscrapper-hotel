import scrapy

class ReviewsSpider(scrapy.Spider):
    name = "tripadvisor-spider"

    # set custom settings
    custom_settings = {
        'FEED_URI': 'file:///C:/Users/acfelk/Documents/IIT_Files/final year/FYP/fyp_workfiles/final_project/backend/drops/%(hotel_name)s-tripadvisor.csv',
        'FEED_FORMAT': 'csv',
    }

    allowed_domains = ["tripadvisor.com"]

    def __init__(self, *args, **kwargs):
        self.hotel_name = kwargs.get('hotel_name')
        self.start_urls = [kwargs.get('start_url')]
        super(ReviewsSpider, self).__init__(*args, **kwargs)
        self.review_count = int(kwargs.get('review_count'))

    revCount = 0

    def parse(self, response):
        for href in response.xpath('//a[contains(@class, "hotels-review-list-parts-ReviewTitle__reviewTitleText")]/@href'):
            if self.revCount >= self.review_count:
                return
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_review)

        next_page = response.xpath('//div[@class="ui_pagination is-centered"]/child::*[2][self::a]/@href')
        if next_page is not None:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_review(self, response):
        rev_content = response.xpath('//span[@class="fullText "]/text()').extract()
        if rev_content is not None and len(rev_content) != 0 and (self.revCount < self.review_count):
            print('EXTRACTING REVIEW ' + str(self.revCount + 1) + ' OUT OF ' + str(self.review_count))
            self.revCount = self.revCount + 1
            yield {
                'text': rev_content,
            }


# USE BELOW COMMAND TO RUN
# scrapy runspider tripadvisor_scrap.py -a hotel_name="GalleFaceHotel" -a start_url="https://www.tripadvisor.com/Hotel_Review-g293962-d2038179-Reviews-Galle_Face_Hotel_Colombo-Colombo_Western_Province.html" -a review_count=100