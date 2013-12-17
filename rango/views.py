# Create your views here.
from django.http import HttpResponse
from django.template import loader, Context
from django.shortcuts import render

def index(request):
	return HttpResponse("Hello world")

def about(request):
	template = loader.get_template('index.html')
	context = Context({'boldmessage':"I am a bold guy"},)
	response = template.render(context)
	return HttpResponse(response)