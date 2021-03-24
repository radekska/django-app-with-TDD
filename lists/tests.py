from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):
	def test_home_page_url_mapping(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)
		html_data = response.content.decode('utf-8')
		
		self.assertTrue(html_data.startswith('<html>'))
		self.assertIn('<title>To-Do lists</title>', html_data)
		self.assertTrue(html_data.endswith('</html>'))
		
		
