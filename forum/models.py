from django.db import models
from django.contrib.auth.models import User

# from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings

from taggit.managers import TaggableManager

# This file contains database for our forum post and comments to our posts. As well there are functionality for reputation

class ForumPost(models.Model):
	CATEGORY = (
		('Important', 'Important'),
		('Suggestions', 'Suggestions'),
		('Help', 'Help'),
		('Question','Question'),
		('Discussion', 'Discussion'),
		('Other', 'Other'),
	)
	# user is already in here defined for owner.py
	user = models.ForeignKey(User, related_name="user_post", blank=True, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=30, null=True)
	topic = models.CharField(max_length=100, null=True, choices=CATEGORY)
	tags = TaggableManager(blank=True)
	
	content = CKEditor5Field(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	post_reputation = models.IntegerField(default=0)
	people_voted = models.IntegerField(default=0)

	def __str__(self):
		return self.topic + ' ' + self.name 

class CommentToPost(models.Model):
	user = models.ForeignKey(User, related_name="user_comment", blank=True, null=True, on_delete=models.CASCADE)
	post = models.ForeignKey(ForumPost, related_name="post_comment", blank=True, null=True, on_delete=models.CASCADE)
	text = models.TextField(null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.post.name + ' ' + self.user.username + ' ' + str(self.date_created) + ' ' + str(self.id)


class Reputation_post(models.Model):

	user = models.ForeignKey(User, related_name="reputation_to_Usermodel", on_delete=models.CASCADE)
	post = models.ForeignKey(ForumPost, related_name="reputation_to_ForumPost", on_delete=models.CASCADE)
	reputation = models.IntegerField(default=0)

	def __str__(self):
		return self.post.name + ' | ' + self.user.username + ' | ' + str(self.reputation)
