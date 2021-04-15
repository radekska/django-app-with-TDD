from .base import FunctionalTest
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
	
	def test_can_start_list_for_one_user(self):
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do list', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h2').text
		self.assertIn('To-Do', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		
		inputbox.send_keys('Buy lambo')
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_table('1: Buy lambo')

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Make tattoo')
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_table('1: Buy lambo')
		self.wait_for_row_in_table('2: Make tattoo')

		# self.fail('Finish the tests!')


	def test_multiple_users_lists_with_different_ulrs(self):
		# user Juliett
		self.browser.get(self.live_server_url)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Make tattoo for Juliett')
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_table('1: Make tattoo for Juliett')

		julietts_lists_url = self.browser.current_url
		self.assertRegex(julietts_lists_url, r'/lists/.+')

		self.browser.quit()
		self.browser = WebDriver()
		
		# user Radoslaw
		self.browser.get(self.live_server_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('1: Make tattoo for Juliett', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Jump from plane')
		inputbox.send_keys(Keys.ENTER)
		self.wait_for_row_in_table('1: Jump from plane')

		radeks_lists_url = self.browser.current_url
		self.assertRegex(radeks_lists_url, r'/lists/.+')
		self.assertNotEqual(radeks_lists_url, julietts_lists_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('1: Make tattoo for Juliett', page_text)
		self.assertIn('1: Jump from plane', page_text)
		self.browser.quit()
