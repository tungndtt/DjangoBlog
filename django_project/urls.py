"""django_project URL Configuration

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
from django.contrib.auth import views
from user.views import register, profile, viewProfile, sendMail, resetPassword
from . import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('blog.urls')),
    path('register/', register, name='Register'),
    path('login/', views.LoginView.as_view(template_name='user/login.html'), name='Login'),
    path('logout/', views.LogoutView.as_view(template_name='user/logout.html'), name='Logout'),
    path('profile/', profile, name='Profile'),
    path('view_profile/<slug:slug>/', viewProfile, name='viewProfile'),
    path('admin/', admin.site.urls),
    path('reset-password/', sendMail, name='Reset_password'),
    path('reset-password/reset/<int:pk>/<slug:hash_password>/', resetPassword, name='Reset_password_confirmation')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
