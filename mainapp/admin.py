from django.contrib import admin

from django_admin_filter.filters import CustomFilter # importing admin filters module

from . models import *

# This file contains all tables, that should be visible from django admin

admin.site.register(Post)
admin.site.register(ContactEmail)
admin.site.register(SecurityEmailMessage)
admin.site.register(CommentToPost)