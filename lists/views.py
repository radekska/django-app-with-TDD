from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

def home_page(request):
	new_item_text = request.POST.get('item_text')

	if request.method == "POST" and new_item_text:
		Item.objects.create(text=new_item_text)
		return redirect('/')

	context = dict(
		items_list=Item.objects.all()
	)

	return render(request, 'home.html', context)
