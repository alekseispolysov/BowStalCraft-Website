from django.contrib import admin

# Register your models here.

# Show admin table to django admin

from . models import *

admin.site.register(User_Profile)
