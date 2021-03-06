from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User goes to app homepage
        self.browser.get(self.live_server_url)

        # The page title mentions to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # She is invited to enter a to-do item right away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Kill all Mormons" in the text box
        inputbox.send_keys("Kill all Mormons")

        # When she hits enter, the page updates, and now lists
        # "1: Kill all Mormons" as item in the to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_and_check_list_in_table('1: Kill all Mormons')
        # time.sleep(1)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("And all the rest")
        inputbox.send_keys(Keys.ENTER)
        # time.sleep(1)

        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #     any(row.text == '1: Kill all Mormons' for row in rows),
        #     f"New to-do item did not appear in the table.\
        #     Contents were:\n{table.text}"
        # )

        # self.assertIn('1: Kill all Mormons', [row.text for row in rows])

        self.wait_and_check_list_in_table('1: Kill all Mormons')
        self.wait_and_check_list_in_table('2: And all the rest')

        # There is a still a text box inviting her to add another item
        # She enters "Kill all Mormons pretenders"

        # The page updates again and now shows two items in the list

        # The site generates a unique url for her -- there is some explanatory
        # text to that effect

        # She visits that URL - her to do list is still there

        # User quits

    def test_multiple_users_can_start_lists_at_diff_urls(self):
        # User starts a new To-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_and_check_list_in_table('1: Buy peacock feathers')

        lists_url = self.browser.current_url
        self.assertRegex(lists_url, '/lists/.+')


        # Now a new user comes to the site
        ## We start a new browser session to make sure no info
        ## is shared between different users
        self.browser.quit()
        self.browser = webdriver.Firefox(options=self.options)

        # New user should not see anything from the previous user's lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # New user enters his own list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy Milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_and_check_list_in_table('1: Buy Milk')

        # New user should also get his own URL
        n_lists_url = self.browser.current_url
        self.assertRegex(n_lists_url, '/lists/.+')
        self.assertNotEqual(n_lists_url, lists_url)

        # Again no trace of previous user's lists
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)

        # Satisfied both users leave
