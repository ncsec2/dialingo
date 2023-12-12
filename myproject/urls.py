"""
URL configuration for myproject project.

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
from django.urls import path
# from myproject.views import hello_world
# from myproject.views import main_page
from myproject import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', views.hello_world, name='hello_world'),
    #음성/텍스트선택
    path('main/', views.main_page, name='main_page'),
    #home
    path('', views.start_page, name='start_page'),
    #음성
    path('voice/', views.voice_page, name='voice_page'),
    #음성
    path('get_voice/', views.get_voice, name='get_voice'),
    #녹음
    path('save_recording/', views.save_recording, name='save_recording'),
    #텍스트
    path('text/', views.text_page, name='text_page'),
    #언어선택
    path('dialect/', views.dialect_page, name='dialect_page')
]
