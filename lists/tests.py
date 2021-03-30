from django.test import TestCase
from lists.models import Item


class ItemModelTest(TestCase):

	def test_saving_and_reading_items(self):
		first_item = Item()
		first_item.text = "The first (ever) list item"
		first_item.save()

		second_item = Item()
		second_item.text = "The second (ever) list item"
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items.get(id=1)
		second_saved_item = saved_items.get(id=2)

		self.assertEqual(first_saved_item.text, "The first (ever) list item")
		self.assertEqual(second_saved_item.text, "The second (ever) list item")







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

	def test_can_save_a_POST_request(self):
		new_item = "A new list item"
		response = self.client.post('/', data={"item_text":new_item})
		self.assertIn(new_item, response.content.decode())
		self.assertTemplateUsed(response, 'home.html')

