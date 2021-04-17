from django.db import models
from django.urls import reverse

class List(models.Model):
	def get_absolute_url(self):
		return reverse("view_list", args=[self.id])
	
class Item(models.Model):
	text = models.TextField(default='')
	item_list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)
	# when deleting List, with models.CASCADE django will delete all items related to that list as well.
	

