from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_cannot_add_empty_list_items(self):
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda :self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda :self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')
        self.wait_for(lambda :self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        self.get_item_input_box().send_keys('Get some rest')
        self.wait_for(lambda :self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_table('1: Buy milk')
        self.wait_for_row_in_table('2: Get some rest')
    
    def test_cannot_add_duplicate_items(self):
        self.browser.get(self.live_server_url)
        self.add_list_item('Buy same car')
        
        self.get_item_input_box().send_keys('Buy same car')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You 've already got this in your list!"
        ))    

    def test_error_messages_are_cleared_on_input(self):
        self.browser.get(self.live_server_url)
        self.add_list_item('Take a shower.')
        self.get_item_input_box().send_keys('Take a shower.')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda : self.assertTrue(
            self.get_error_element().is_displayed()))

        self.get_item_input_box().send_keys('Typing...')
        self.wait_for(lambda : self.assertFalse(
            self.get_error_element().is_displayed()))

    def test_error_messages_are_cleared_on_mouse_click(self):
        self.browser.get(self.live_server_url)
        self.action_chains = ActionChains(self.browser)

        self.add_list_item('Brush your teeth.')
        self.get_item_input_box().send_keys('Brush your teeth.')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for(lambda : self.assertTrue(
            self.get_error_element().is_displayed()))

        self.action_chains.click(self.get_item_input_box()).perform()
        self.wait_for(lambda : self.assertFalse(
            self.get_error_element().is_displayed()))



