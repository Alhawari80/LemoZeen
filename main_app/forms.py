from django.forms import ModelForm
from django import forms

from .models import Trip , Driver

class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = ['destination', 'date_time','location','notes']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['name', 'image']