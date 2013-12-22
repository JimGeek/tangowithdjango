# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context, RequestContext
from django.shortcuts import render, render_to_response
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserProfileForm, ProfileForm
from django.contrib.auth import authenticate,login,logout
from datetime import datetime

def index(request):
	user = request.user
	context = RequestContext(request)
	cat_list = Category.objects.order_by('id')[:6]
	for category in cat_list:
		category.url = category.name.replace(' ','_')
	pages = Page.objects.order_by('-views')[:5]
	# response = render_to_response('index.html', {'pages':pages,'categories':cat_list,'user':user}, context)

	# visits = int(request.COOKIES.get('visits','0'))

	# if request.COOKIES.has_key('last_visit'):
	# 	last_visit = request.COOKIES['last_visit']
	# 	print last_visit
	# 	# print datetime.strptime(last_visit[:7],"%Y-%m-%d %H:%M:%S")
	# 	last_visit_time = datetime.strptime(last_visit[:19],"%Y-%m-%d %H:%M:%S")
	# 	if (datetime.now() - last_visit_time).total_seconds() > 60 :
	# 		response.set_cookie('visits',visits+1)
	# 		response.set_cookie('last_visit',datetime.now())
	# else:
	# 	response.set_cookie('last_visit',datetime.now())
		
	# return response
	if request.session.get('last_visit'):
		last_visit_time = request.session.get('last_visit')
		visits = request.session.get('visits',0)

		if (datetime.now() - datetime.strptime(last_visit_time[:19],"%Y-%m-%d %H:%M:%S")).total_seconds() > 60:
			request.session['visits'] = visits+1
			request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = 1


	return render_to_response('index.html', {'pages':pages,'categories':cat_list,'user':user}, context)

def about(request):

	if request.session.get('visits'):
		visits = request.session.get('visits')
	else:
		visits = 0
	template = loader.get_template('about.html')
	context = Context({'boldmessage':"I am a bold guy",'visits':visits},)
	response = template.render(context)
	return HttpResponse(response)

def category(request, category_name_url):
	context = RequestContext(request)
	category_name = category_name_url.replace('_',' ')
	context_dict = {'category_name':category_name}

	try:
		category = Category.objects.get(name=category_name)
		context_dict['category'] = category

		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages

		context_dict['category_name_url']= category_name_url

	except Category.DoesNotExist:
		pass

	return render_to_response('category.html', context_dict, context)

def add_category(request):
	context = RequestContext(request)

	if request.method == 'POST':
		form = CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)
			return index(request)

		else:
			print form.errors
	else:
		form = CategoryForm()

	return render_to_response('add_category.html',{'form':form},context)

def add_page(request, category_name_url):
	context = RequestContext(request)
	category_name = category_name_url.replace('_',' ')

	if request.method == 'POST':
		form = PageForm(request.POST)

		if form.is_valid():
			page = form.save(commit = False)
			cat = Category.objects.get(name=category_name)
			page.category = cat
			page.views = 0
			page.save()

			return category(request, category_name_url)

	else:
		page = PageForm()

	return render_to_response('add_page.html', {'category_name':category_name, 'page':page, 'category_name_url':category_name_url}, context)

def register(request):
	context = RequestContext(request)
	registered = False 

	if request.method == 'POST':
		user_form = ProfileForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)
			profile.user = user

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()
			registered = True

		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = ProfileForm()
		profile_form = UserProfileForm()

	return render_to_response('register.html',{'user_form':user_form, 'profile_form':profile_form, 'registered':registered}, context)

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username,password=password)

		if user is not None:
			if user.is_active:

				login(request,user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("You are blocked from this site")
		else:
			print "Invalid deatail entered"
			return HttpResponse("Invalid credential entered")
	else:
		pass
	return render_to_response('login.html',{},context)

def user_logout(request):
	context = RequestContext(request)
	logout(request)
	
	return HttpResponseRedirect('/')