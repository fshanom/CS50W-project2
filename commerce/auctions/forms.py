from django import forms
from .models import AuctionItem, Bids

class ItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ('name', 'description', 'image',  'category', 'current_price')

        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'description' : forms.Textarea(attrs={'class': 'form-control'}),
            'image' : forms.TextInput(attrs={'class': 'form-control','label':'Image URL'}),
            'category' : forms.RadioSelect(attrs={'class': 'checkbox form-check-row'}),
            'current_price' : forms.NumberInput(attrs={'class': 'form-control','min':0, 'placeholder':'$'})

        }
        labels = {
            'image' : 'Image URL',
            'current_price' : 'Initial Price'
        }

class BidsForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['value']

        widgets = {
            'value' : forms.NumberInput(attrs={'class': 'form-control','min':0, 'placeholder':'$'})
        }
        labels = {
            'value' : 'Bid Value'
        }
