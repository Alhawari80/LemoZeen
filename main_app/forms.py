from django.forms import ModelForm
from django import forms

from .models import Trip , Driver ,Car , Profile

class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = "__all__" 
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'image']