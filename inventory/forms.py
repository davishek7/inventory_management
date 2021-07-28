from django import forms
from .models import Product, Location, Movement


class LocationForm(forms.ModelForm):
    name = forms.CharField(label='',required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3','placeholder':'Location name'}))

    class Meta:
        model = Location
        fields = ('name',)
        

class ProductForm(forms.ModelForm):
    name = forms.CharField(label='',required=True, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3','placeholder':'Product name'}))
    qty = forms.IntegerField(label='',widget=forms.TextInput(
        attrs={'class': 'form-control mb-3','placeholder':'Product quantity'}))

    class Meta:
        model = Product
        fields = ('name', 'qty',)


class MovementForm(forms.ModelForm):
    location_to = forms.ModelChoiceField(
        queryset=Location.objects.all(), empty_label="----Select Location----",
        widget=forms.Select(
            attrs={'class': 'form-control form-control-sm mb-3'}),
        required=True, label='Location'
    )

    class Meta:
        model = Movement
        fields = ('location_to',)
