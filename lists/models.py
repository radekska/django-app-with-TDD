from django.db import models

class List(models.Model):
	pass

class Item(models.Model):
	text = models.TextField(default='')
	item_list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
	# when deleting List, with models.CASCADE django will delete all items related to that list as well.
	

