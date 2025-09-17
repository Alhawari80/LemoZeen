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
    cars = Car.objects.filter(user=request.user)
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


def add_trip(request, car_id):
    form = TripForm(request.POST)
    cat = Car.objects.get(id=car_id)
    
    # feeding_form = FeedingForm(request.POST or None)
    if form.is_valid():
        new_trip = form.save(commit=False)
        new_trip.car_id = car_id
        new_trip.save()
    return redirect('detail', car_id=car_id)

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