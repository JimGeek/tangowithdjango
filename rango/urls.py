from django.http import HttpResponse 
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$','rango.views.index'),
	url(r'^about/$','rango.views.about'),
	url(r'^add_category/$', 'rango.views.add_category'),
	url(r'^category/(?P<category_name_url>\w+)/add_page/$','rango.views.add_page'),
	url(r'^category/(?P<category_name_url>\w+)/$', 'rango.views.category', name='category'),
	url(r'^register/$', 'rango.views.register'),
	url(r'^login/$','rango.views.user_login'),
	url(r'^logout/$','rango.views.user_logout'),
	)