from django.test import TestCase
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class ListModelTest(TestCase):
    def test_absolute_url(self):
        list_ = List.objects.create()
        self.assertEqual(list_.get_absolute_url(), f'/lists/{list_.id}/')

class ItemModelTest(TestCase):

    def test_cannot_save_empty_list_items(self):
        list_ = List.objects.create()
        item = Item(list=list_, text='')
        with self.assertRaises(ValidationError):
            item.save()
            item.full_clean()

    def test_default_text(self):
        item = Item()
        self.assertEqual(item.text, '')

    def test_item_is_related_to_list(self):
        list_ = List.objects.create()
        item = Item.objects.create(list=list_)
        self.assertIn(item, list_.item_set.all())

    def test_string_representation(self):
        item = Item(text='Sample')
        self.assertEqual(str(item), 'Sample')

    def test_list_ordering(self):
        list_ = List.objects.create()
        item1 = Item.objects.create(text='Sample 1', list=list_)
        item2 = Item.objects.create(text='Sample 2', list=list_)
        item3 = Item.objects.create(text='Sample 3', list=list_)
        self.assertEqual(list(Item.objects.all()), [item1, item2, item3])


    def test_form_saves_handles_saving_to_a_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'Sample'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'Sample')
        self.assertEqual(new_item.list, list_)

    def test_duplicate_list_items_are_invalid(self):
        list_ = List.objects.create()
        Item.objects.create(text='Sample', list=list_)
        with self.assertRaises(IntegrityError):
            item = Item(text='Sample', list=list_)
            item.save()

    def test_can_save_same_item_to_differet_lists(self):
        text = 'Sample'
        list1 = List.objects.create()
        list2 = List.objects.create()
        Item.objects.create(text=text, list=list1)
        item2 = Item(text=text, list=list2)
        item2.full_clean()
