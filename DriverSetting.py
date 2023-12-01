# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.service import Service
from selenium import webdriver

service = Service(
    executable_path="/home/irfan/programs/git/tcdd-bilet-yer-kontrol/chromedriver")
#driver = webdriver.Chrome(service=service)


class DriverSetting:
    def driverUP(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1920,1080')
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        #driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
