"""
URL configuration for passwordMan project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from . import views

urlpatterns = [

    path('', views.landing, name='landing'),
    path('signUp/', views.signUp, name='signUp'),
    path('login/', views.login, name='login'),
    path('passwordEntry/', views.passwordEntry, name='confirmation'),
    path('login/loginLanding/', views.loginLanding, name='passwordEntry'),
    path('passwordVault/', views.passwordVault, name='passwordEntry'),
    path('passwordEntry/addDuplicate/', views.addDuplicate, name='addDuplicate'),
    # URL pattern for rendering the password generator page.
    path('generate_password/', views.password_generator, name='generate_password'),
    # URL pattern for the AJAX request to generate a new password.
    path('generate-password-ajax/', views.generate_password_ajax, name='generate_password_ajax'),
]
