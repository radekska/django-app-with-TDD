from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List

def home_page(request):
	return render(request, 'home.html')


def view_list(request):
	context = dict(
		items_list=Item.objects.all()
	)

	return render(request, 'list.html', context)

def new_list(request):
	item_list = List.objects.create()
	Item.objects.create(text=request.POST['item_text'], item_list=item_list)
	return redirect('/lists/the-only-list-in-the-world/')
