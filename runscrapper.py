import subprocess

class RevScrapperDetail:
    hotel_name = ''
    review_count = 0
    tripadvisor_url = ''
    bookingdotcom_url = ''

class RunScrapper:
    # SET
    # HOTEL_NAME = % ~1
    # SET
    # START_URL = % ~2
    # SET
    # REVIEW_COUNT = % ~3

    def trip_advisor(self, hotel_name, hotel_url, review_count):

        # hotel_name = "GFH"
        # hotel_url = "https://www.tripadvisor.com/Hotel_Review-g293962-d2038179-Reviews-Galle_Face_Hotel_Colombo-Colombo_Western_Province.html"
        # review_count = "5"

        item = subprocess.Popen(["scrapper/tripadvisor_scrap.bat", hotel_name, hotel_url, review_count], shell=True, stdout=subprocess.PIPE)

        for line in item.stdout:
            print(line)

    def booking_dot_com(self, hotel_name, hotel_url, review_count):

        # hotel_name = "GFH"
        # hotel_url = "https://www.booking.com/hotel/lk/galle-face.en-gb.html"
        # review_count = "5"

        item = subprocess.Popen(["scrapper/bookingdotcom_scrap.bat", hotel_name, hotel_url, review_count], shell=True, stdout=subprocess.PIPE)

        for line in item.stdout:
            print(line)

    def run(self, rev_scrapper_detail):
        try:
            if rev_scrapper_detail.tripadvisor_url != '' and rev_scrapper_detail.bookingdotcom_url != '':
                self.trip_advisor(rev_scrapper_detail.hotel_name, rev_scrapper_detail.tripadvisor_url, str(rev_scrapper_detail.review_count))
                self.booking_dot_com(rev_scrapper_detail.hotel_name, rev_scrapper_detail.bookingdotcom_url, str(rev_scrapper_detail.review_count))
            elif rev_scrapper_detail.tripadvisor_url != '':
                self.trip_advisor(rev_scrapper_detail.hotel_name, rev_scrapper_detail.tripadvisor_url, str(rev_scrapper_detail.review_count))
            else:
                self.booking_dot_com(rev_scrapper_detail.hotel_name, rev_scrapper_detail.bookingdotcom_url, str(rev_scrapper_detail.review_count))
            return 'success'
        except:
            return 'fail'


# runscrapper = RunScrapper()
# runscrapper.trip_advisor("GFH", "https://www.tripadvisor.com/Hotel_Review-g293962-d2038179-Reviews-Galle_Face_Hotel_Colombo-Colombo_Western_Province.html", "5")
# runscrapper.booking_dot_com("GFH", "https://www.booking.com/hotel/lk/galle-face.en-gb.html", "5")