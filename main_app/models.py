from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
TRIPS = (
    ('M', 'Morning'),
    ('A', 'Afternoon'),
    ('E', 'Evening'),
    ('N', 'Night'),
)

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
    date_time = models.DateTimeField()
    car = models.ForeignKey(Car,on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    notes = models.TextField(max_length=250)
    # driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.car.name} {self.get_car_display()} on {self.date}"
    
    
    
    
