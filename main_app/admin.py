from django.contrib import admin
from .models import Car, Trip, Driver, Profile

# Register your models here.
admin.site.register(Car)
admin.site.register(Trip)
admin.site.register(Driver)
admin.site.register(Profile)