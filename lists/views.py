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
			Item.objects.create(text=request.POST['text'], item_list=items_list)
			return redirect(items_list)
			
	context = dict(
		items_list = List.objects.get(id=list_id),
		form=form
	)
	return render(request, 'list.html', context)

def new_list(request):
	form = ItemForm(data=request.POST)
	if form.is_valid():
		new_item_list = List.objects.create()
		new_text = request.POST.get('text')
		Item.objects.create(text=new_text, item_list=new_item_list)
	else:
		return render(request, 'home.html', {'form': form})

	return redirect(new_item_list)

