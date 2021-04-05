from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
	return render(request, 'home.html')


def view_list(request, list_id):
	context = dict(
		items_list = List.objects.get(id=list_id)
	)
	return render(request, 'list.html', context)

def new_list(request):
	new_item_list = List.objects.create()

	new_item_text = request.POST.get('item_text')
	Item.objects.create(text=new_item_text, item_list=new_item_list)
	return redirect(f'/lists/{new_item_list.id}/')

def add_item(request, list_id):
	existing_item_list = List.objects.get(id=list_id)

	new_item_text = request.POST.get('item_text')
	Item.objects.create(text=new_item_text, item_list=existing_item_list)
	return redirect(f'/lists/{existing_item_list.id}/')



	
