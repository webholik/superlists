from django.shortcuts import render, redirect
# from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm
from django.core.exceptions import ValidationError


def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.ecreate(text=request.POST['item_text'])
    #     return redirect('/lists/01/')
    # else:
    return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    # items = Item.objects.filter(list=list_)
    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "You can't have an empty list item"

    return render(request, 'list.html', {'list': list_, 'error': error})


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(list_)
