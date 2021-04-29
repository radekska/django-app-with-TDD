from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os
import time
import unittest

MAX_WAIT = 10

def wait(func):
	def inner(*args, **kwargs):
		start_time = time.time()
		while True:
			try:
				return func(*args, **kwargs)
			except (AssertionError, WebDriverException) as exception:
				if time.time() - start_time > MAX_WAIT:
					raise exception
				time.sleep(0.5)	
	return inner


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

	@wait
	def wait_for(self, func):
		return func()

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	
	@wait
	def wait_for_row_in_table(self, input_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(input_text, [row.text for row in rows], 
			f"New to-do item did not apper in the table \nContents are: {table.text}")

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)