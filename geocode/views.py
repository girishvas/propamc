from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import generic
from django.utils import timezone
from django.core.mail import send_mail, send_mass_mail, EmailMultiAlternatives
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta, date
import os.path, time
from django.conf import settings

import django_excel as excel
import xlrd
from xlrd import open_workbook
import requests
from .models import *


def getCordinates(address):
	address 		= address
	api_key 		= 'AIzaSyAQgQxaLyual4d-C2Ro8l--zULv98X1NBs'
	api_response 	= requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
	api_dict 		= api_response.json()

	if api_dict['status'] == 'OK':
		latitude 	= api_dict['results'][0]['geometry']['location']['lat']
		longitude 	= api_dict['results'][0]['geometry']['location']['lng']
		result 		= {"lat":latitude, "long":longitude}
	else:
		latitude 	= None
		longitude 	= None
	return result


class HomePage(TemplateView):
	template_name 		= 'index.html'
	
	def get(self, request, *args, **kwargs):
		location 		= Location.objects.all().order_by('-id')
		
		paginator 		= Paginator(location, 25)
		page 			= request.GET.get('page')
		try:
			location 	= paginator.page(page)
		except PageNotAnInteger:
			location 	= paginator.page(1)
		except EmptyPage:
			location 	= paginator.page(paginator.num_pages)

		return render(request, self.template_name, locals())

	def post(self, request, *args, **kwargs):
		if 'file' in request.FILES and ((request.FILES['file'].name.endswith('.xls')) or (request.FILES['file'].name.endswith('.xlsx'))):
			if not request.FILES['file'].multiple_chunks():
				im 				= request.FILES['file'].name
				ext 			= os.path.splitext(im)[1]

				# ext_c 			= 'upload_' + str(int(time.time())) + ext
				ext_c 			= request.FILES['file'].name

				c 				= request.FILES.get('file')
				path 			= settings.MEDIA_ROOT+'/'+ext_c

				destination 	= open(path, 'wb+')
				for chunk in c.chunks():
					destination.write(chunk)
				destination.close()
				
				book 			= open_workbook(path)
				sheet 			= book.sheet_by_index(0)
				keys 			= [sheet.cell(0, col_index).value for col_index in range(sheet.ncols)]

				head 			= []
				for row_index in range(0, sheet.nrows):
					d 			= [sheet.cell(row_index, col_index).value for col_index in range(sheet.ncols)]
					head.append(d)
					break

				dict_ls 		= []
				for row_index in range(1, sheet.nrows):
					d 			= {keys[col_index]: sheet.cell(row_index, col_index).value for col_index in range(sheet.ncols)}
					dict_ls.append(d)

				if head[0][0] == 'name' and head[0][1] == 'address':
					if len(dict_ls) == 0:
						status 	= 'Blank'
						error 	= None
					else:
						for x in dict_ls:
							cordinates = getCordinates(x['address'])
							locobj 				= Location()
							locobj.name 		= x['name']
							locobj.address 		= x['address']
							locobj.latitude 	= cordinates["lat"]
							locobj.longitude 	= cordinates["long"]
							locobj.save()
				else:
					return HttpResponse('Date is not in the expected format ( Name, Address ), please download the sample file.')
				return HttpResponseRedirect('/')
			else:
				return HttpResponse('File is too large!')
		else:
			return HttpResponse('Error! Please upload proper excel (.xls, .xlsx) files only!')


class Download(TemplateView):
	def get(self, request, *args, **kwargs):
		query_sets 	= Location.objects.all()
		column_names = ['name', 'address', 'latitude', 'longitude']
		return excel.make_response_from_query_sets(
			query_sets,
			column_names,
			'xls',
			file_name="download"
		)