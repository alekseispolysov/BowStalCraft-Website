from django import forms
from django.forms import ModelForm
from captcha.fields import CaptchaField
from . models import *

# This file contains 3 form four our tables for: comment for news, contact e-mail table and report message  

class CommentToPostForm(ModelForm):
	text = forms.CharField(widget=forms.Textarea, label='')
	class Meta:
		model = CommentToPost
		fields = ['text']

class ContactEmailsForm(ModelForm):
	
	class Meta:
		model = ContactEmail
		fields= '__all__'
		exclude = ('date_sent',)
		

class SecutiryMainForm(ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = SecurityEmailMessage
		fields = '__all__'
		exclude = ('date_sent',)
		