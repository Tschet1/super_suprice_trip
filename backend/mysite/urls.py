"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from google_maps.views import get_directions_view
from api.views import surprise_me, le_preferences

urlpatterns = [
    path('admin/', admin.site.urls),
    path('instrutions/get', get_directions_view, name='get_directions_view'),
    path('api/surprize', surprise_me, name='surprise_me'),
    path('api/preferences', le_preferences, name='le_preferences'),
]
