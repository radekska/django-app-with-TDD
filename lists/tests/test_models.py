from django.core.exceptions import ValidationError
from django.test import TestCase
from lists.models import Item, List


class ItemModelTest(TestCase):

	def test_default_text(self):
		item = Item()
		self.assertEqual(item.text, '')

	def test_item_is_related_to_list(self):
		item_list = List.objects.create()
		item = Item()

		item.item_list = item_list
		item.save()
		self.assertIn(item, item_list.item_set.all())

	def test_cannot_save_empty_list_item(self):
		item_list = List()
		item_list.save()
		
		item = Item(item_list=item_list, text='')

		with self.assertRaises(ValidationError):
			item.save()
			item.full_clean()

	def test_duplicate_items_are_invalid(self):
		item_list = List.objects.create()
		Item.objects.create(item_list=item_list, text='same testing text')
		with self.assertRaises(ValidationError):
			item = Item(item_list=item_list, text='same testing text')
			item.full_clean()

	def test_can_save_same_item_to_different_lists(self):
		list_1 = List.objects.create()
		list_2 = List.objects.create()

		Item.objects.create(item_list=list_1, text='same testing text')
		item = Item(item_list=list_2, text='same testing text')
		item.full_clean() # should not raise.

	def test_list_ordering(self):
		list_1 = List.objects.create()
		item_1 = Item.objects.create(item_list=list_1, text='item 1')
		item_2 = Item.objects.create(item_list=list_1, text='item 2')
		item_3 = Item.objects.create(item_list=list_1, text='item 3')

		self.assertEqual(
			list(Item.objects.all()),
			[item_1, item_2, item_3]
		)

	def test_string_representation(self):
		item = Item(text='testing text')
		self.assertEqual(str(item), 'testing text')


class ListModelTest(TestCase):

	def test_get_absolute_url(self):
		item_list = List.objects.create()
		self.assertEqual(item_list.get_absolute_url(), f'/lists/{item_list.id}/')



