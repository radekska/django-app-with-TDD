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

	def make_post_request(self):
		new_item = "A new list item"
		return self.client.post('/', data={"item_text":new_item})
		
	def test_use_of_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_can_save_a_POST_request(self):
		new_item = "A new list item"
		self.make_post_request()
		self.assertTrue(Item.objects.count())
		self.assertTrue(new_item, Item.objects.get(text=new_item).text)

	def test_redirects_after_post(self):
		response = self.make_post_request()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')

	def test_if_saves_items_when_necessary(self):
		self.client.get('/')
		self.assertEqual(Item.objects.count(), 0)


class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_all_items(self):
		Item.objects.create(text='item one')
		Item.objects.create(text='item two')

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'item one')
		self.assertContains(response, 'item two')





