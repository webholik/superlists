from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'item_next':'New item'})

        self.assertEqual(Item.objects.count(),1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'New item')

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_next':'New item'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(response['location'], '/lists/01/')

        # self.assertIn('New item', response.content.decode())
        # self.assertTemplateUsed(response,'home.html')

    def test_only_save_items_when_necessary(self):
        response = self.client.get('/')
        self.assertEqual(Item.objects.count(),0,
                         "Saving empty items for GET request"
                         )



class ListViewTest(TestCase):

    def test_display_all_items(self):
        Item.objects.create(text='item1')
        Item.objects.create(text='item2')

        response = self.client.get('/lists/01/')

        # self.assertIn('item1', response.content.decode())
        # self.assertIn('item2', response.content.decode())
        self.assertContains(response, 'item1')
        self.assertContains(response, 'item2')

    def test_uses_list_template(self):
        response = self.client.get('/lists/01/')
        self.assertTemplateUsed(response,'list.html')

class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first item"
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_item.text, first_saved_item.text)
