from django.contrib import admin

from . models import *

# This is our admin files for Forum app

admin.site.register(ForumPost)

admin.site.register(CommentToPost)

admin.site.register(Reputation_post)

