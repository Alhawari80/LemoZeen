from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

#add a Trip model
from django.db import models
from django.conf import settings
from decimal import Decimal
# Create your models here.
TRIPS = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening'),
    ('N', 'Night'),
)

ROLES = [
    ('A', 'Admin'),
    ('D', 'Driver'),
    ('U', 'User'),
]



# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLES)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Driver(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    
    def __str__(self):
        return f"{self.name}"

    ##To go to details after viewing the driver
    def get_absolute_url(self):
        return reverse('drivers_detail', kwargs={'pk': self.id})

# class Car(models.Model):
#     name = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#     plate_number = models.TextField(max_length=250)
#     year = models.IntegerField()
#     image = models.ImageField(upload_to='main_app/static/uploads/', default="")
#     drivers = models.ManyToManyField(Driver)
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

from django.core.validators import MinValueValidator, MaxValueValidator
import datetime

class Car(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    plate_number = models.TextField(max_length=250)
    year = models.IntegerField(
        validators=[
            MinValueValidator(1980),
            MaxValueValidator(datetime.date.today().year)
        ],
        default=datetime.date.today().year
    )
    image = models.ImageField(upload_to='main_app/static/uploads/', default="")
    drivers = models.ManyToManyField(Driver)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    
#to display the name and year of the car
    def __str__(self):
        return f"{self.name} {self.year}"

#to go to details after viewing the car
    def get_absolute_url(self):
        return reverse('detail',kwargs={'car_id': self.id})


class Trip(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    car = models.ForeignKey('Car', on_delete=models.CASCADE)               # adjust string if Car in another app
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    origin_address = models.CharField(max_length=255)
    origin_lat = models.DecimalField(max_digits=9, decimal_places=6)
    origin_lng = models.DecimalField(max_digits=9, decimal_places=6)
    destination_address = models.CharField(max_length=255)
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6)
    destination_lng = models.DecimalField(max_digits=9, decimal_places=6)
    distance_text = models.CharField(max_length=50, blank=True)
    duration_text = models.CharField(max_length=50, blank=True)
    route_polyline = models.TextField(blank=True)     # optional for storing overview_polyline
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Trip {self.id} {self.origin_address} → {self.destination_address}"
    
    # driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.car.name} {self.get_car_display()} on {self.date}"
    
    
    
    
