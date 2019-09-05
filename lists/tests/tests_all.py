from django.test import TestCase
from django.urls import resolve
from lists.views import home_page
from django.http import HttpRequest
from lists.models import Item,List

class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    # def test_can_save_a_POST_request(self):
    #     response = self.client.post('/', data={'item_next':'New item'})

    #     self.assertEqual(Item.objects.count(),1)
    #     new_item = Item.objects.first()
    #     self.assertEqual(new_item.text, 'New item')

    # def test_redirects_after_POST(self):
    #     response = self.client.post('/', data={'item_next':'New item'})
    #     self.assertEqual(response.status_code,302)
    #     self.assertEqual(response['location'], '/lists/01/')

    #     # self.assertIn('New item', response.content.decode())
    #     # self.assertTemplateUsed(response,'home.html')

    # def test_only_save_items_when_necessary(self):
    #     response = self.client.get('/')
    #     self.assertEqual(Item.objects.count(),0,
    #                      "Saving empty items for GET request"
    #                      )



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
        response = self.client.post(f'/lists/{correct_list.id}/')
        self.assertEqual(response.context['list'], correct_list)

class ListAndItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "The second item"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(saved_list, list_)
        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_item.text, first_saved_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, second_item.text)
        self.assertEqual(second_saved_item.list, list_)


class NewListTest(TestCase):

    def test_can_save_POST_request(self):
        self.client.post('/lists/new', data={
            'item_next':'A new list item'})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new list item')

    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={
            'item_next':'A new list item'
        })
        # self.assertEqual(response.status_code, 302)
        # self.assertEqual(response['location'],'lists/01/')
        new_list = List.objects.first()
        self.assertRedirects(response, f'/lists/{new_list.id}/')

    def test_can_save_POST_request_to_existing_list(self):
        print("Can save Post")
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={
            'item_next' : 'New item for existing list',
        })

        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.list, correct_list)
        self.assertEqual(new_item.text, 'New item for existing list')

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={
            'item_next' : 'New item for existing list',
        })

        self.assertRedirects(response, f'/lists/{correct_list.id}/')


