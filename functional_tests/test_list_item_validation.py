from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
	
	def test_cannot_add_empty_list_items(self):
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		self.wait_for(lambda :self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have empty list item!"
		))

		self.get_item_input_box().send_keys('Buy milk')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_table('1: Buy milk')

		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for(lambda :self.assertEqual(
			self.browser.find_element_by_css_selector('.has-error').text,
			"You can't have empty list item!"
		))

		self.get_item_input_box().send_keys('Get some rest')
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_table('1: Buy milk')
		self.wait_for_row_in_table('2: Get some rest')
	