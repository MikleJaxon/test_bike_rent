from django.contrib import admin

from django.contrib import admin
from .models import Bike, Rental

admin.site.register(Bike)
admin.site.register(Rental)