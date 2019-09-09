from django.test import TestCase
from lists.forms import (ItemForm, ExistingListItemForm,
                         DUPLICATE_ITEM_ERROR, EMPTY_ITEM_ERROR)
from lists.models import List, Item


class ItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css(self):
        form = ItemForm()
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR],
        )


class ExistingListItemFormTest(TestCase):

    def test_form_item_input_has_placeholder_and_css(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn('placeholder="Enter a to-do item"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [EMPTY_ITEM_ERROR],
        )

    def test_form_validation_for_duplicate_items(self):
        list_ = List.objects.create()
        Item.objects.create(text='Sample', list=list_)
        form = ExistingListItemForm(for_list=list_, data={'text': 'Sample'})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['text'],
            [DUPLICATE_ITEM_ERROR]
        )
