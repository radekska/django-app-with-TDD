from django.core.exceptions import ValidationError
from django import forms
from lists.models import Item

# class ItemForm(forms.Form):
#     item_text = forms.CharField(
#         widget=forms.fields.TextInput(attrs={
#             'placeholder': 'Enter a to-do item',
#             'class': 'form-control input-md'
#         }),
#     )

EMPTY_ITEM_ERROR = "You can't have empty list item!"
DUPLICATE_ITEM_ERROR = "You 've already got this in your list!"

# Will use ModelForm as it uses form validation directly from model.
class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
            'placeholder': 'Enter a to-do item',
            'class': 'form-control input-md'
            })
        }

        error_messages = {
            'text': {'required':EMPTY_ITEM_ERROR}
            }

    def save(self, for_list):
        self.instance.item_list = for_list
        return super().save()

class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.item_list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)

    def save(self):
        return forms.models.ModelForm.save(self)