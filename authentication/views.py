from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib import messages

from . models import *
from . forms import *

# View file, that is showing our views for authentication
# registration form view
register_template = 'authentication/registration.html'

class RegistrationPage(View):
	def get(self, request):
		if request.user.is_authenticated:
			return redirect('mainapp:home-page')

		form = CreateUserForm()
		ctx = {
		'form':form,
		}

		return render(request, register_template, ctx)
	def post(self, request):
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password1')
			user_auth = authenticate(username=username, password=password)
			login(request, user_auth)
			# all after form login defined in signals
			
			return redirect('mainapp:home-page')
		else:
			#not refresh the form, because otherwise errors won't be returned
			la = 'hello world'
			ctx = {
			'form':form,
			'hi':la,
			}
			return render(request, register_template, ctx)

# User profile page view. This is view for user for himself, not others. He can edit himself
class UserProfile(LoginRequiredMixin, View):
	def get(self, request):
		user = User.objects.get(pk=request.user.id)
		user_profile = request.user.user_profile
		form1 = UserProfileForm(instance=user)
		form2 = ProfileUserForm(instance=user_profile)
		ctx = {
		'user':user,
		'form1':form1,
		'form2':form2,
		}
		return render(request, 'authentication/user_profile.html', ctx)

	def post(self, request):
		user_profile = request.user.user_profile
		user = User.objects.get(pk=request.user.id)
		form1 = UserProfileForm(request.POST, instance=user)
		form2 = ProfileUserForm(request.POST, request.FILES, instance=user_profile)

		if form1.is_valid() and form2.is_valid():
			form1.save()
			form2.save()
			return redirect('authentication:user-profile')
		else:
			ctx = {
			'form1':form1,
			'form2':form2,
			}
			return render(request, 'authentication/user_profile.html', ctx)

# This is view for other users to be able to view other user
class ViewProfilePage(View):
	def getqueryrelation(self, request, assessed):
		# function that is taking everything that repeating in it. It is checking if user has a query relation with post. If he liked or disliked that post
		# also it checks, if user is authenticated
		if request.user.is_authenticated:
			query_relation = Reputation_user.objects.filter(appraiser=request.user).filter(assessed=assessed).first()
			if query_relation is None:
				relation_value = 0
			else:
				relation_value = query_relation.reputation
		else:
			relation_value = None

		return relation_value

	def get(self, request, pk):
		user_object = User.objects.get(pk=pk)
		ctx={
		'user_object':user_object,
		'relation_value': self.getqueryrelation(request, user_object),
		}
		return render(request, 'authentication/user_profile_view.html', ctx)

# this thing is made with ajax. It is view profile with ajax to be able to edit reputation
# this whole view is made to be able to edit reputation of the concrete user
class ViewProfilePageAJAX(LoginRequiredMixin, View):
	def post(self, request, pk):
		# get the user Entry.objects.get(pk=1)
		appraiser_user = User.objects.get(pk=request.POST["user_appraiser_id"])

		# get assessed user
		assessed_user = User.objects.get(pk=request.POST["user_assessed_id"])

		assessed_user_profile = User_Profile.objects.get(pk=assessed_user.id)

		# get user action
		user_action = request.POST["user_action"]


		if assessed_user.is_staff or assessed_user==appraiser_user:
			return JsonResponse()

		# make a assessment here
		# temp reputation
		if user_action == 'dislike':
			reputation_temp = 1
		else:
			reputation_temp = -1


		# get query relation
		query_relation = Reputation_user.objects.filter(appraiser=appraiser_user).filter(assessed=assessed_user).first()

		counter = 0


		if query_relation == None:
			if user_action == 'like':
				reputation_temp = 1
			elif user_action == 'dislike':
				reputation_temp = -1
			else:
				reputation_temp = 0
			new_relation = Reputation_user(appraiser=appraiser_user, assessed=assessed_user, reputation=reputation_temp)
			
			assessed_user_profile.reputation += new_relation.reputation
			assessed_user_profile.save()
			new_relation.save()
			query_relation = new_relation
		else:
			# so if reputation is greater then 0 we will check if
			if query_relation.reputation > 0:
				# it is like pressed, if so, undo the reputation and lover the people, that have been before
				if user_action == 'like':
					query_relation.reputation += -1
					counter = -1
					
				# if it is dislike, we dont undo the people, but we changing the reputation
				elif user_action == 'dislike':
					query_relation.reputation += -2
					counter = -2
				else:
				# else we do nothing
					pass
			# else if the reputation is negative (means the dislike have been pressed before)
			elif query_relation.reputation < 0:
				# we will check, if it is a like, if so we won't change the count of people, inseted change reputation
				if user_action == 'like':
					query_relation.reputation += 2
					counter += 2
				# if dislike have been pressed the second time, we will undo dislike and lower the people
				elif user_action == 'dislike':
					query_relation.reputation += 1
					
					counter +=1
				# else we do nothing
				else:
					pass
			# if the relation exist and it is 0 and something have been pressed we will change reputation and do nothing with people, because they are counted up
			else:
				if user_action == 'like':
					query_relation.reputation = 1
					counter += 1
					
				elif user_action == 'dislike':
					query_relation.reputation = -1
					
					counter -= 1
				else:
					pass			
			assessed_user_profile.reputation += counter
			assessed_user_profile.save()
			query_relation.save()

		data = {
		
		"reputation" : assessed_user_profile.reputation,
		"current_relation_reputation": query_relation.reputation
		}
		
		return JsonResponse(data)