from django.db import models
from django.utils import timezone


class Location(models.Model):
	name 		= models.CharField(max_length=80)
	address 	= models.CharField(max_length=600, null=True, blank=True)
	latitude 	= models.CharField(max_length=40, null=True, blank=True)
	longitude 	= models.CharField(max_length=40, null=True, blank=True)
	added_On 	= models.DateTimeField(auto_now_add=True, null=True)
	updated_On 	= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = "Location"
		verbose_name_plural = "Locations"