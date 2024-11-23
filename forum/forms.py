from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from . models import *

# This forms file contains forum creation and comment creation functionality

# Here we have functionality to be able to create post for forum
class ForumPostForm(ModelForm):
	class Meta:
		model = ForumPost
		fields = ['name', 'topic', 'tags', 'content']

# This is functionality to be able to create comment for post
class CommentToPostForm(ModelForm):
	text = forms.CharField(widget=forms.Textarea, label='')
	class Meta:
		model = CommentToPost
		fields = ['text']
