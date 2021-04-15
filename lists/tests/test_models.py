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