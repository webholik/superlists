from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from lists.models import Item,List
from django.utils.html import escape
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)



class ListViewTest(TestCase):

    def test_display_correct_items(self):
        correct_list_ = List.objects.create()
        Item.objects.create(text='item1', list=correct_list_)
        Item.objects.create(text='item2', list=correct_list_)

        other_list_ = List.objects.create()
        Item.objects.create(text='other item1',list=other_list_)
        Item.objects.create(text='other item2', list=other_list_)

        response = self.client.get(f'/lists/{correct_list_.id}/')

        # self.assertIn('item1', response.content.decode())
        # self.assertIn('item2', response.content.decode())
        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')
        self.assertNotContains(response, 'other item1')
        self.assertNotContains(response, 'other item2')

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertTemplateUsed(response,'list.html')

    def test_passes_correct_list_to_template(self):
        other_list = List.objects.create()
        correct_list = List.objects.create()
        response = self.client.get(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_POST_request_to_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={
            'text' : 'New item for existing list',
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, correct_list)
        self.assertEqual(new_item.text, 'New item for existing list')

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/',
            data={
            'text' : 'New item for existing list',
        })

        self.assertRedirects(response, f'/lists/{correct_list.id}/')

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get(f'/lists/{list_.id}/')
        self.assertIsInstance(response.context['form'], ItemForm)
        self.assertContains(response, 'name="text"')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            f'/lists/{list_.id}/',
            {'text':''}
        )
        
    def test_invalid_input_nothing_saved_to_database(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_invalid_input_renders_test_template(self):
        response = self.post_invalid_input()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('list.html')
    
    def test_invalid_input_shows_error_on_the_page(self):
        response = self.post_invalid_input()
        expected_error = escape(EMPTY_ITEM_ERROR)
        self.assertContains(response, expected_error)


class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={
            'text':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={
            'text':'A new list item'
        })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'],'lists/01/')
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={'text': ''})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={'text':''})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new/', data={'text':''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(List.objects.count(), 0)


