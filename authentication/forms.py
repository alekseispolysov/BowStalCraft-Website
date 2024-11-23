from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from . models import *

# in this file we create User form, authentication form, user edit probile form/ We need this to make users able to edit themselves
class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def __init__(self, *args, **kwargs):
		super(CreateUserForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

class AuthenticationForm(AuthenticationForm):
	class Meta:
		model = User
		fields = ('email', 'password')


class UserProfileForm(ModelForm):
	class Meta:
		model = User	
		fields = ['username', 'first_name', 'last_name']


class ProfileUserForm(ModelForm):
	class Meta:
		model = User_Profile
		fields = '__all__'
		exclude = ['user', 'reputation', 'opinion_posts']
