from django.db import models
from django.urls import reverse


class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    text = models.TextField(default='')
    # When deleting List, with models.CASCADE django will delete all items related to that list as well.
    item_list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

    # Sets of field names that, taken together, must be unique:
    class Meta:
        # The id ordering for the object, for use when obtaining lists of objects:
        ordering = ('id',)
        # Sets of field names that, taken together, must be unique:
        unique_together = ('item_list', 'text')

    def __str__(self):
        return self.text
