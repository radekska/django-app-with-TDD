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

