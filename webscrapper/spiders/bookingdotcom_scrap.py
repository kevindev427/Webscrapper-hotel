import scrapy

class ReviewsSpider(scrapy.Spider):
    name = "bookingdotcom-spider"

    # set custom settings
    custom_settings = {
        'FEED_URI': 'file:///C:/Users/acfelk/Documents/IIT_Files/final year/FYP/fyp_workfiles/final_project/backend/drops/%(hotel_name)s-bookingscom.csv',
        'FEED_FORMAT': 'csv'
    }

    allowed_domains = ["booking.com"]

    def __init__(self, *args, **kwargs):
        self.hotel_name = kwargs.get('hotel_name')
        self.start_urls = [kwargs.get('start_url')]
        super(ReviewsSpider, self).__init__(*args, **kwargs)
        self.review_count = int(kwargs.get('review_count'))

    def parse(self, response):
        all_review_url = response.xpath('.//*[@class="show_all_reviews_btn"]/@href').extract_first()

        if all_review_url is not None:
            review_url = "https://booking.com" + all_review_url
            yield scrapy.Request(review_url, callback=self.parse_review)

    revCount = 0

    def parse_review(self, response):
        allreviewsinpage = response.xpath('.//*[@itemprop="review"]')

        for eachreview in allreviewsinpage:
            neg_rev = eachreview.xpath('.//p[@class="review_neg "]/*[@itemprop="reviewBody"]/text()').extract_first()
            pos_rev = eachreview.xpath('.//p[@class="review_pos "]/*[@itemprop="reviewBody"]/text()').extract_first()

            if pos_rev is not None and (self.revCount <= self.review_count):
                print('EXTRACTING REVIEW ' + str(self.revCount) + ' OUT OF ' + str(self.review_count))
                self.revCount = self.revCount + 1
                yield {
                    'text': pos_rev,
                }

            if neg_rev is not None and (self.revCount <= self.review_count):
                print('EXTRACTING REVIEW ' + str(self.revCount) + ' OUT OF ' + str(self.review_count))
                self.revCount = self.revCount + 1
                yield {
                    'text': neg_rev,
                }

        next_page = response.xpath('.//*[@class="page_link review_next_page"]/a/@href').extract_first()
        if next_page is not None and (self.revCount <= self.review_count):
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(next_page_url, callback=self.parse_review)


# USE BELOW COMMAND TO RUN
# scrapy runspider bookingdotcom_scrap.py -a hotel_name="GalleFaceHotel_bookingscom" -a start_url="https://www.booking.com/hotel/lk/galle-face.en-gb.html" -a review_count=1000