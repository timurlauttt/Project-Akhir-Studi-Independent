"""
URL configuration for questify_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from questify_app import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', views.index, name='index'),
    path('', RedirectView.as_view(url='/landing-page/', permanent=True)),  # Redirect ke landing-page
    path('landing-page/', views.index, name='landing-page'),
    path('', include('questify_app.urls')),
    path('accounts/', include('allauth.urls')),
]
