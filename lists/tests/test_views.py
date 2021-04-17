from django.test import TestCase
from django.utils.html import escape
from lists.models import Item, List
from lists.forms import ItemForm


class HomePageTest(TestCase):		
	def test_use_of_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')

	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)
	


class ListViewTest(TestCase):
	def setUp(self):
		self.new_text = 'A new item to existing list.'

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

	def test_can_save_POST_request_to_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			f'/lists/{correct_list.id}/',
			data={'text':self.new_text}
			)
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		
		self.assertEqual(new_item.text, self.new_text)
		self.assertEqual(new_item.item_list, correct_list)

	def test_post_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			f'/lists/{correct_list.id}/',
			data={'text':self.new_text}
			)

		self.assertRedirects(response, f'/lists/{correct_list.id}/')

	def test_validation_errors_on_list_page(self):
		items_list = List.objects.create()
		response = self.client.post(
			f'/lists/{items_list.id}/',
			data={'text':''}
		)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'list.html')

		expected_error = escape("You can't have empty list item!")
		self.assertContains(response, expected_error)

class NewListTest(TestCase):
	def __make_post_request(self, new_item="A new list item"):
		return self.client.post('/lists/new', data={"text":new_item})

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

	def test_validation_errors_are_sent_back(self):
		response = self.__make_post_request(new_item='')
		
		self.assertEqual(200, response.status_code)
		self.assertTemplateUsed(response, 'home.html')

		expected_error = escape("You can't have empty list item!")
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.__make_post_request(new_item='')

		self.assertEqual(Item.objects.count(), 0)
		self.assertEqual(List.objects.count(), 0)



