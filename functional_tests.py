from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()

	def tearDown(self):
		self.browser.quit()

	def test_list_creation_and_retrive(self):	
		self.browser.get("http://localhost:8000")
		self.assertIn('To-Do lists', self.browser.title)
		self.fail("Finish the test later")

if __name__ == "__main__":
	unittest.main()
