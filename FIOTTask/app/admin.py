from django.contrib import admin

from .models import Weather
# Register your models here.
admin.site.register([Weather])  # Register your models here, e.g., admin.site.register(YourModel)