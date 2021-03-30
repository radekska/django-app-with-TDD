from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def check_if_exists_in_table(self, input_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(input_text, [row.text for row in rows], 
			f"New to-do item did not apper in the table \nContents wher {table.text}")

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

		self.check_if_exists_in_table('1: Buy lambo')
		self.check_if_exists_in_table('2: Make tattooo')

		self.fail('Finish the tests!')

if __name__ == "__main__":
	unittest.main()
