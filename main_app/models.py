from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

#add a Trip model

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
from django.contrib.auth.decorators import login_required

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
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
    origin_address = models.CharField(max_length=255)
    origin_lat = models.DecimalField(max_digits=9, decimal_places=6)
    origin_lng = models.DecimalField(max_digits=9, decimal_places=6)
    destination_address = models.CharField(max_length=255)
    destination_lat = models.DecimalField(max_digits=9, decimal_places=6)
    destination_lng = models.DecimalField(max_digits=9, decimal_places=6)
    distance_text = models.CharField(max_length=50, blank=True)
    duration_text = models.CharField(max_length=50, blank=True)
    route_polyline = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    


    def __str__(self):
        return f"Trip {self.id}: {self.origin_address} → {self.destination_address}"

    
    
    
    @login_required
    def create_trip(request):
        if request.method == "POST":
            car_id = request.POST.get("car_id")
            driver_id = request.POST.get("driver_id")

            # required fields
            origin_address = request.POST.get("origin_address")
            destination_address = request.POST.get("destination_address")

            # hidden fields from JS
            origin_lat = request.POST.get("origin_lat")
            origin_lng = request.POST.get("origin_lng")
            destination_lat = request.POST.get("destination_lat")
            destination_lng = request.POST.get("destination_lng")
            route_polyline = request.POST.get("route_polyline")
            distance_text = request.POST.get("distance_text")
            duration_text = request.POST.get("duration_text")

            # fetch related objects
            car = get_object_or_404(Car, id=car_id)
            driver = Driver.objects.filter(id=driver_id).first() if driver_id else None

            # create Trip instance
            trip = Trip.objects.create(
                user=request.user,
                car=car,
                driver=driver,
                origin_address=origin_address,
                origin_lat=origin_lat or 0,
                origin_lng=origin_lng or 0,
                destination_address=destination_address,
                destination_lat=destination_lat or 0,
                destination_lng=destination_lng or 0,
                route_polyline=route_polyline or "",
                distance_text=distance_text or "",
                duration_text=duration_text or ""
            )

            # redirect to detail page (make sure you have this view/template)
            return redirect("trip_detail", trip.id)

        return redirect("home")

    def trip_detail(request, pk):
        trip = get_object_or_404(Trip, pk=pk)
        return render(request, "trips/detail.html", {"trip": trip})