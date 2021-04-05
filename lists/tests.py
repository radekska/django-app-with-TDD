from django.test import TestCase
from lists.models import Item, List


class ListAndItemModelTest(TestCase):

	def test_saving_and_reading_items(self):
		item_list = List()
		item_list.save()

		first_item = Item()
		first_item.text = "The first (ever) list item"
		first_item.item_list = item_list
		first_item.save()

		second_item = Item()
		second_item.text = "The second (ever) list item"
		second_item.item_list = item_list
		second_item.save()

		saved_list = List.objects.first()
		self.assertEqual(saved_list, item_list)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items.get(id=1)
		second_saved_item = saved_items.get(id=2)

		self.assertEqual(first_saved_item.text, "The first (ever) list item")
		self.assertEqual(first_saved_item.item_list, item_list)

		self.assertEqual(second_saved_item.text, "The second (ever) list item")
		self.assertEqual(second_saved_item.item_list, item_list)



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


class ListViewTest(TestCase):
	def test_uses_list_template(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_all_items(self):
		item_list = List.objects.create()
		Item.objects.create(text='item one', item_list=item_list)
		Item.objects.create(text='item two', item_list=item_list)

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'item one')
		self.assertContains(response, 'item two')


class NewListTest(TestCase):
	def __make_post_request(self):
		new_item = "A new list item"
		return self.client.post('/lists/new', data={"item_text":new_item})

	def test_can_save_a_POST_request(self):
		new_item = "A new list item"
		self.__make_post_request()
		self.assertEqual(Item.objects.count(), 1)
		self.assertTrue(new_item, Item.objects.get(text=new_item).text)

	def test_redirects_after_post(self):
		response = self.__make_post_request()
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')




