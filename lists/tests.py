from django.test import TestCase

class HomePageTest(TestCase):
	# def test_home_page_url_mapping(self):
	# 	found = resolve('/')
	# 	self.assertEqual(found.func, home_page)

	# def test_home_page_returns_correct_html(self):
	# 	request = HttpRequest()
	# 	response = home_page(request)
	# 	html_data = response.content.decode('utf-8')
	# 	expected_html_data = render_to_string('home.html')
	# 	self.assertEqual(html_data, expected_html_data)

		
	def test_use_of_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')