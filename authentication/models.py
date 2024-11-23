from django.db import models
from django.contrib.auth.models import User

from forum.models import ForumPost

# In this file we make Database tables for authentication and user profiles

# this is a fix for standard djnago table User
# quick fix to user model, without writing in it
# email must be unique, required and if it is already in db no blow up
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = True

# user profile table
class User_Profile(models.Model):
	# add options of gender -> male or female
	GENDER = (
		('Male', 'Male'),
		('Female', 'Female'),
		('Other', 'Other'),	
		)

	user = models.OneToOneField(User, related_name="user_profile", blank=True, null=True, on_delete=models.CASCADE)
	
	date_of_birth = models.DateField(blank=True, null=True)

	gender = models.CharField(max_length=15, null=True, blank=True, choices=GENDER)

	profile_picture = models.ImageField(default="user_default_images/default_user_picture.png", null=True, blank=True)

	description = models.TextField(max_length=450, null=True, blank=True)


	# change reputation to the int field (change datatype + apply reputation schema)
	reputation = models.IntegerField(default="0")

	opinion_posts = models.ManyToManyField(ForumPost, blank=True)


	def __str__(self):
		try:
			return self.user.username
		except:
			print('Something went wrong, while loading user.username, probably, because something missing in database')
			return 'Err'

# reputation table 
class Reputation_user(models.Model):
	# Reputaion giver
	appraiser = models.ForeignKey(User, related_name="Appraiser_to_Usermodel", on_delete=models.CASCADE)
	# User who recieves reputation
	assessed = models.ForeignKey(User, related_name="Assessed_to_ForumPost", on_delete=models.CASCADE)
	
	reputation = models.IntegerField(default=0)

	def __str__(self):
		return self.appraiser.username + ' | ' + self.assessed.username + ' | ' + str(self.reputation)

