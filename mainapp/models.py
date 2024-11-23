from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

# This file contains all database talbes for our mainapp


# -------------------------------------------- ckeditor
class Article(models.Model):
    title=models.CharField('Title', max_length=200)
    text=CKEditor5Field('Text', config_name='extends')
# ck eidotr -------------------------------------------


# This our post talbe for news
class Post(models.Model):
	name = models.CharField(max_length=30, null=True)
	text = CKEditor5Field(null=True, blank=True)
	preview_text = models.CharField(max_length=400, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)
	preview_picture = models.ImageField(default="home_posts/sample_image.jpg", null=True, blank=True)

	def __str__(self):
		return self.name

# comment on post table
class CommentToPost(models.Model):
	user = models.ForeignKey(User, related_name="user_comment_news", blank=True, null=True, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, related_name="post_comment_news", blank=True, null=True, on_delete=models.CASCADE)
	text = models.TextField(null=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return str(self.date_created) + ' ' + self.post.name + ' ' + self.user.username

# contact us with email table
class ContactEmail(models.Model):
	email = models.EmailField(max_length=30, null=True)
	subject = models.CharField(max_length=50, null=True)
	text = models.TextField(null=True)
	date_sent = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.subject + ' ' + self.email

# Security report table
class SecurityEmailMessage(models.Model):
	CATEGORY = (
		('Bug on website', 'Bug on website'),
		('Violation', 'Violation'),
		('Suggestions', 'Suggestions'),
		('Help', 'Help'),
		('Bug on server','Bug on server'),
		('Bug with plugins', 'Bug with plugins'),
		('Other', 'Other'),
	)
	email = models.EmailField(max_length=30, null=True)
	subject = models.CharField(max_length=50, null=True)
	topic = models.CharField(max_length=100, null=True, choices=CATEGORY)
	text = CKEditor5Field(null=True)
	date_sent = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.subject + ' ' + self.topic + ' ' + self.email