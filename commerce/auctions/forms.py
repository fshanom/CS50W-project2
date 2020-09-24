from django import forms
from .models import AuctionItem, Bids

class ItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ('name', 'description', 'image',  'category')

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'image' : forms.TextInput(attrs={'class': 'form-control','label':'Image URL'}),
            'category' : forms.CheckboxSelectMultiple(attrs={'class': 'checkbox form-check-row'}),
        }
        labels = {
            'image' : 'Image URL'
        }

class BidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['value']

        widgets = {
            'value' : forms.NumberInput(attrs={'class': 'form-control','min':0, 'placeholder':'$'})
        }
