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
		item_list = List.objects.create()
		response = self.client.get(f'/lists/{item_list.id}/')
		self.assertTemplateUsed(response, 'list.html')


	def test_displays_items_for_specific_list(self):
		specific_list = List.objects.create()
		Item.objects.create(text='item one', item_list=specific_list)
		Item.objects.create(text='item two', item_list=specific_list)

		specific_list_next = List.objects.create()
		Item.objects.create(text='next item one', item_list=specific_list_next)
		Item.objects.create(text='next item two', item_list=specific_list_next)


		response = self.client.get(f'/lists/{specific_list.id}/')

		self.assertContains(response, 'item one')
		self.assertContains(response, 'item two')
		self.assertNotContains(response, 'next item one')
		self.assertNotContains(response, 'next item two')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['items_list'], correct_list)


class NewItemTest(TestCase):
	def setUp(self):
		self.new_item_text = 'A new item to existing list.'


	def test_can_save_POST_request_to_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text':self.new_item_text}
			)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		
		self.assertEqual(new_item.text, self.new_item_text)
		self.assertEqual(new_item.item_list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text':self.new_item_text}
			)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')



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
		new_list = List.objects.first()
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, f'/lists/{new_list.id}/')




