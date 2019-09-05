from functional_tests.base import FunctionalTest
from selenium.webdriver.common.keys import Keys
from unittest import skip

class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # Archak goes to home page and accidently tries to submit an empty list item
        # He hits Enter on the empty list item

        # The page reloads to show an error message, saying that the list cannot be blanked

        # He then enter some text in the input box and presses Enter, which works as expected

        # Perversely he tries again to submit an empty list but this time again he gets the
        # error message

        self.fail('Write me')