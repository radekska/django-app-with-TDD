from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os
import time
import unittest

MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		super().setUpClass()
		cls.browser = WebDriver()

		staging_server = os.environ.get('STAGING_SERVER')
		if staging_server:
			cls.live_server_url = f'http://{staging_server}'

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
