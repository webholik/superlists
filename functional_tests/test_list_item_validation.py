from .base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip


class ItemValidationTest(FunctionalTest):
    def get_error_item(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        # Archak goes to home page and accidently tries to submit an empty list item
        # He hits Enter on the empty list item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The browser intercepts the request and does not load the list page
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_new_item:invalid'
        ))

        # He then enter some text in the input box and the error disappears
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_new_item:valid'
        ))

        # And he can submit it successfully
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_and_check_list_in_table('1: Buy milk')

        # Perversely he tries again to submit an empty list but this time again he gets
        # stopped by the browser
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.browser.find_element_by_css_selector(
            '#id_new_item:invalid'
        ))

        # So he gives up his devious ways and enters the actual text in the input
        self.browser.find_element_by_id(
            'id_new_item').send_keys('Buy cigarette')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_and_check_list_in_table('2: Buy cigarette')

    def test_cannot_add_duplicate_list_items(self):
        self.browser.get(self.live_server_url)
        textbox = self.browser.find_element_by_id('id_new_item')
        textbox.send_keys('Buy Milk')
        textbox.send_keys(Keys.ENTER)

        self.wait_and_check_list_in_table('1: Buy Milk')

        textbox = self.browser.find_element_by_id('id_new_item')
        textbox.send_keys('Buy Milk')
        textbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_item().text,
            "You've already got this in your list"))

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        textbox = self.browser.find_element_by_id('id_new_item')
        textbox.send_keys('Buy Milk')
        textbox.send_keys(Keys.ENTER)
        self.wait_and_check_list_in_table('1: Buy Milk')
        textbox = self.browser.find_element_by_id('id_new_item')
        textbox.send_keys('Buy Milk')
        textbox.send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_item().is_displayed()
        ))

        textbox = self.browser.find_element_by_id('id_new_item')
        textbox.send_keys('Buy kerosene')
        self.wait_for(lambda: self.assertFalse(
            self.get_error_item().is_displayed()
        ))