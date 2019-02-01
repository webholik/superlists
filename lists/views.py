from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item,List

def home_page(request):
    # if request.method == 'POST':
    #     Item.objects.create(text=request.POST['item_next'])
    #     return redirect('/lists/01/')
    # else:
    return render(request, 'home.html')

def view_list(request):
    return render(request, 'list.html', {'items':Item.objects.all()})

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_next'],list=list_)
    return redirect('/lists/01/')
