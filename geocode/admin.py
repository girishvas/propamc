from django.contrib import admin
from .models import *


class LocationAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'latitude', 'longitude', 'added_On')
	list_filter = ['added_On']
	search_fields = ['name', 'address']

admin.site.register(Location, LocationAdmin)
