from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
	return render(request, 'home.html', {'form': ItemForm()})


def view_list(request, list_id):
	items_list = List.objects.get(id=list_id)
	error = None

	if request.method == 'POST':
		try:
			item = Item(text=request.POST['item_text'], item_list=items_list)
			item.full_clean()
			item.save()
			return redirect(items_list)
		except ValidationError:
			error = "You can't have empty list item!"
			
	context = dict(
		items_list = List.objects.get(id=list_id),
		error=error
	)
	return render(request, 'list.html', context)

def new_list(request):
	new_item_list = List.objects.create()

	new_item_text = request.POST.get('item_text')
	item = Item(text=new_item_text, item_list=new_item_list)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		new_item_list.delete()
		error = "You can't have empty list item!"
		return render(request, 'home.html', {'error':error})

	return redirect(new_item_list)

