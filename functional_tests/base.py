from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
import os

MAX_WAIT = 3


class FunctionalTest(StaticLiveServerTestCase):
    options = webdriver.FirefoxOptions()
    def setUp(self):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
            
        self.options.add_argument('--headless')
        self.browser = webdriver.Firefox(options=self.options)

    def wait_and_check_list_in_table(self, text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def wait_for(self, func):
        start_time = time.time()
        while True:
            try:
                return func()
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def tearDown(self):
        self.browser.quit()
    
