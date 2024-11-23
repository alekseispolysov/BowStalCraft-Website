from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import path
from . import views
from . forms import *
from django.urls import path, include

app_name = 'authentication'

# Urls for authentication app

urlpatterns = [
	path('register/', views.RegistrationPage.as_view(), name='register-new-user-page'),
	path('login/',
		auth_views.LoginView.as_view(authentication_form=AuthenticationForm, template_name="authentication/login.html"),
		name="login"),
	path('logout/',
		auth_views.LogoutView.as_view(template_name="authentication/login.html"),
		name="logout"),	
    path('reset_password/',
     	auth_views.PasswordResetView.as_view(template_name="authentication/password_reset_form.html", email_template_name="authentication/password_reset_email.html", success_url=reverse_lazy("authentication:password_reset_done")), 
    	name="reset_password",),

    path('reset_password_sent/', 
    	auth_views.PasswordResetDoneView.as_view(template_name="authentication/password_reset_done.html"), 
    	name="password_reset_done"),
    
    path('reset/<uidb64>/<token>/', 
    	auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html", success_url=reverse_lazy("authentication:password_reset_complete") ), 
    	name="password_reset_confirm"),
    
    path('reset_password_complete/', 
    	auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"), 
    	name="password_reset_complete"),	

	path('profile/', views.UserProfile.as_view(), name='user-profile'),

	path('profile/<str:pk>/', views.ViewProfilePage.as_view(), name='user-view-profile'),

    path('profile/<str:pk>/ajax/', views.ViewProfilePageAJAX.as_view()),
]

