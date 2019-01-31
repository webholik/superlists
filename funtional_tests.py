from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes to app homepage
        self.browser.get("http://localhost:8000")

        # The page title mentions to-do lists
        assert 'To-Do' in self.browser.title

        # She is invited to enter a to-do item right away

        # She types "Kill all Mormons" in the text box

        # When she hits enter, the page updates, and now lists
        # "1: Kill all Mormons" as item in the to-do list

        # There is a still a text box inviting her to add another item
        # She enters "Kill all Mormons pretenders"

        # The page updates again and now shows two items in the list

        # The site generates a unique url for her -- there is some explanatory
        # text to that effect

        # She visits that URL - her to do list is still there

        # User quits


if __name__ == '__main__':
    unittest.main(warnings='ignore')
