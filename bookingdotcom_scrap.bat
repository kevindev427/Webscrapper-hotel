@echo off
setlocal
SET HOTEL_NAME=%~1
SET START_URL=%~2
SET REVIEW_COUNT=%~3

call pushd "C:\Users\acfelk\Documents\IIT_Files\final year\FYP\fyp_workfiles\final_project\backend\scrapper\webscrapper\spiders"
call scrapy runspider "C:\Users\acfelk\Documents\IIT_Files\final year\FYP\fyp_workfiles\final_project\backend\scrapper\webscrapper\spiders\bookingdotcom_scrap.py" -a hotel_name=%HOTEL_NAME% -a start_url=%START_URL% -a review_count=%REVIEW_COUNT%

endlocal