from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_list_creation_and_retrive(self):	
		self.browser.get("http://localhost:8000")
		self.assertIn('To-Do lists', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'), 'Enter a to-do item')
		
		inputbox.send_keys('Buy lambo')
		inputbox.send_keys(Keys.ENTER)
		time.sleep(1)

		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(any(row.text == '1: Buy lambo' for row in rows), "New to-do item did not apper in the table")
		
		self.fail('Finish the tests!')

if __name__ == "__main__":
	unittest.main()
