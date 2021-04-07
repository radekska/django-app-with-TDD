from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time
import unittest

MAX_WAIT = 10


class NewVisitorTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.browser = WebDriver()

	@classmethod
	def tearDownClass(cls):
		cls.browser.quit()
		super().tearDownClass()


	def wait_for_row_in_table(self, input_text):
		start_time = time.time()
		while True:
			try:
				table = self.browser.find_element_by_id('id_list_table')
				rows = table.find_elements_by_tag_name('tr')
				self.assertIn(input_text, [row.text for row in rows], 
					f"New to-do item did not apper in the table \nContents are: {table.text}")
				return None
			except (AssertionError, WebDriverException) as exception:
				if time.time() - start_time > MAX_WAIT:
					raise exception
				time.sleep(0.5)

	def test_can_start_list_for_one_user(self):
		self.browser.get(self.live_server_url)
		self.assertIn('To-Do list', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h1').text
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



	def test_layout_and_style(self):
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512, delta=10
			)

		inputbox.send_keys('Testing')
		inputbox.send_keys(Keys.ENTER)

		self.wait_for_row_in_table('1: Testing')

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512, delta=10
			)




















































# No need to use that anymore as from now on will be using Django test runner for FTs.
# if __name__ == "__main__":
# 	unittest.main()
