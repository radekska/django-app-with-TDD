from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm, EMPTY_ITEM_ERROR

def home_page(request):
	return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
	items_list = List.objects.get(id=list_id)
	form = ItemForm()

	if request.method == 'POST':
		form = ItemForm(request.POST)
		if form.is_valid():
			form.save(for_list=items_list)
			return redirect(items_list)
			
	return render(request, 'list.html', {
		'items_list': items_list,
		'form': form
	})

def new_list(request):
	form = ItemForm(data=request.POST)
	if form.is_valid():
		new_item_list = List.objects.create()
		form.save(for_list=new_item_list)
	else:
		return render(request, 'home.html', {'form': form})

	return redirect(new_item_list)

