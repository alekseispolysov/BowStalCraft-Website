from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

# importing it cause i have to send success login messages
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in

from . models import *

# After we creating user, we create his profile

# after we create user, we create a profile for him
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
	if created:
		instance = get_object_or_404(User, username=instance.username)
		user_profile = User_Profile(user=instance)
		user_profile.save()

# success login message
def logged_in_message(sender, user, request, **kwargs):
	"""
	Add a welcome message when the user logs in
	"""
	user_name = request.user.username
	messages.success(request, f"You are now logged in as {user_name}.")


user_logged_in.connect(logged_in_message)



