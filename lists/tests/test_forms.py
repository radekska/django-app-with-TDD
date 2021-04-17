from django.test import TestCase
from lists.forms import (
    EMPTY_ITEM_ERROR, DUPLICATE_ITEM_ERROR,
    ItemForm, ExistingListItemForm
)
from lists.models import Item, List

class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item', form.as_p())
        self.assertIn('form-control input-md', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_save_handles_saving_to_a_list(self):
        item_list = List.objects.create()
        form = ItemForm(data={'text': 'testing form'})
        new_item = form.save(for_list=item_list)

        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'testing form')
        self.assertEqual(new_item.item_list, item_list)


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        item_list = List.objects.create()
        form = ExistingListItemForm(for_list=item_list)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())

    def test_form_validation_for_blank_items(self):
        item_list = List.objects.create()
        form = ExistingListItemForm(for_list=item_list, data={'text':''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])

    def test_form_validation_for_duplicate_items(self):
        item_list = List.objects.create()
        Item.objects.create(item_list=item_list, text='no duplicates')
        form = ExistingListItemForm(for_list=item_list, data={'text':'no duplicates'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        item_list = List.objects.create()
        form = ExistingListItemForm(for_list=item_list, data={'text':'testing text'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.first())
