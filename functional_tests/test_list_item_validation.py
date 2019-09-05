from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Archak goes to home page and accidently tries to submit an empty list item
        # He hits Enter on the empty list item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # The page reloads to show an error message, saying that the list cannot be blanked
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))
        # He then enter some text in the input box and presses Enter, which works as expected
        self.browser.find_element_by_id('id_new_item').send_keys('Buy milk')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Perversely he tries again to submit an empty list but this time again he gets the
        # error message
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # So he gives up his devious ways and enters the actual text in the input
        self.browser.find_element_by_id('id_new_item').send_keys('Buy cigarette')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy cigarette')