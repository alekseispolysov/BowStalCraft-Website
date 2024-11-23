"""bowcraftorg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# doing data because need to set up static url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, re_path


# rest framework
from rest_framework import routers

from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# from ckeditor_uploader import views as ckeditor_views

# This file is main file for our project urls

# rest framework
router = routers.DefaultRouter()

# Here we have url paths to all our applications

# Apps, that we are using: admin app, authenication, forum, mainappp

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('django_admin_filter.urls')),
    path('', include('mainapp.urls')),
    path('user/', include('authentication.urls')),
    path('forum/', include('forum.urls')),
    path('ckeditor/', login_required(include('ckeditor_uploader.urls'))),
    # path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include(router.urls)),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Here we add other paths to our project, like captcha, Mediroot, 404 page

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    path('captcha/', include('captcha.urls')),
]

def test_404_view(request):
    raise Http404("Page not found")

urlpatterns += [
    path('test-404/', test_404_view, name='test_404_view'),
]