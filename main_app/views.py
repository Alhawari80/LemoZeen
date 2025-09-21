from urllib import request
from django.shortcuts import redirect, render
# from django.http import HttpResponse
from .models import Car, Driver, Trip 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .forms import TripForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin  #to protect classes

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.views.decorators.http import require_POST
from .models import Car, Driver, Trip  


@login_required
def profile(request):
    return render(request, 'users/profile.html')

class CarCreate(LoginRequiredMixin, CreateView):
    model = Car
    fields = ['name','model','plate_number','year','image']
    # success_url = '/cars'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CarUpdate(LoginRequiredMixin, UpdateView):
    model = Car
    fields = ['name','model','plate_number','year','image']
    # success_url = '/cars'

class CarDelete(LoginRequiredMixin, DeleteView):
    model = Car
    success_url = '/cars'

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def cars_index(request):
    #select all cars from the database (main_app_car)
    # cars = Car.objects.filter(user=request.user)
    cars = Car.objects.all()
    return render(request, 'cars/index.html', {'cars': cars})

@login_required
def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    #Get the trips the car doesn't have
    drivers_car_doesnt_have = Driver.objects.exclude(id__in = car.drivers.all().values_list('id', flat=True))
    trip_form = TripForm()
    return render(request, 'cars/detail.html', {'car': car, 
                'trip_form': trip_form,
                'drivers': drivers_car_doesnt_have
                })

@login_required
def user_trips(request):
    trips = Trip.objects.filter(user=request.user)
    return render(request, 'cars/user_trips.html', {'trips': trips})

@login_required
def all_trips(request):
    trips = Trip.objects.all()
    return render(request, 'cars/all_trips.html', {'trips': trips})

def add_trip(request, car_id):
    form = TripForm(request.POST)
    car = Car.objects.get(id=car_id)
    # user = user.object.get(id=user_id)
    

    if form.is_valid():
        new_trip = form.save(commit=False)
        new_trip.car_id = car_id
        new_trip.save()
    return redirect('detail', car_id=car_id)

def book_trip(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    drivers = Driver.objects.all()  # or filter by available
    return render(request, 'main_app/book_trip.html', {
        'car': car,
        'drivers': drivers,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })

@require_POST
def create_trip(request):
    # Basic server-side payload validation:
    car = get_object_or_404(Car, pk=request.POST.get('car_id'))
    driver_id = request.POST.get('driver_id') or None
    driver = Driver.objects.get(pk=driver_id) if driver_id else None
    origin_address = request.POST.get('origin_address', '')
    destination_address = request.POST.get('destination_address', '')
    try:
        origin_lat = Decimal(request.POST.get('origin_lat'))
        origin_lng = Decimal(request.POST.get('origin_lng'))
        destination_lat = Decimal(request.POST.get('destination_lat'))
        destination_lng = Decimal(request.POST.get('destination_lng'))
    except Exception:
        # handle bad input
        return redirect('book_trip', car_id=car.id)

    distance_text = request.POST.get('distance_text', '')
    duration_text = request.POST.get('duration_text', '')
    route_polyline = request.POST.get('route_polyline', '')

    trip = Trip.objects.create(
        user = request.user if request.user.is_authenticated else None,
        car = car,
        driver = driver,
        origin_address = origin_address,
        origin_lat = origin_lat,
        origin_lng = origin_lng,
        destination_address = destination_address,
        destination_lat = destination_lat,
        destination_lng = destination_lng,
        distance_text = distance_text,
        duration_text = duration_text,
        route_polyline = route_polyline,
    )
    return redirect('trip_detail', trip_id=trip.id)

def trip_detail(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    return render(request, 'main_app/trip_detail.html', {
        'trip': trip,
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })

# CBV's for Drivers Model
class DriverCreate(LoginRequiredMixin, CreateView):
    model = Driver
    fields = ['name',  'image'] #or '__all__'  to add all fields
    # success_url = '/drivers'

class DriverUpdate(LoginRequiredMixin, UpdateView):
    model = Driver
    fields = ['name', 'image']
    # success_url = '/drivers'

class DriverDelete(LoginRequiredMixin, DeleteView):
    model = Driver
    success_url = '/drivers'

class DriverList(LoginRequiredMixin, ListView):
    model = Driver
    template_name = 'drivers/list.html'

class DriverDetail(LoginRequiredMixin, DetailView):
    model = Driver



@login_required
def assoc_driver(request, car_id, driver_id):
  # Add this driver_id with the car selected
  Car.objects.get(id=car_id).drivers.add(driver_id)
  return redirect('detail', car_id=car_id)

@login_required
def unassoc_driver(request, car_id, driver_id):
  # Remove the driver_id from the car selected
  Car.objects.get(id=car_id).drivers.remove(driver_id)
  return redirect('detail', car_id=car_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again later'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

from django.conf import settings
from django.shortcuts import render

def map_view(request):
    return render(request, "map.html", {
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })


import googlemaps
from django.conf import settings

def geocode_address(address):
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    result = gmaps.geocode(address)
    return result
def geocode_view(request):
    address = request.GET.get('address', '')
    geocode_result = None
    if address:
        geocode_result = geocode_address(address)
    return render(request, 'geocode.html', {
        'geocode_result': geocode_result,
        'address': address,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })