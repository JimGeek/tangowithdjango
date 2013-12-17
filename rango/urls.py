from django.http import HttpResponse 
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','rango.views.index'),
	url(r'^about/$','rango.views.about'),
	)