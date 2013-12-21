from django import forms 
from rango.models import Category, Page, UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text='Please enter the category name')
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Category

class PageForm(forms.ModelForm):
	title = forms.CharField(max_length=120, help_text='Enter the title for the page')
	url = forms.URLField(max_length=200, help_text='Enter the URL for the page')
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Page

		fields = ('title','url', 'views')

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields =('website','picture')

class ProfileForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username','email','password')