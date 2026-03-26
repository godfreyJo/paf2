from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('join/', views.join, name='join'),
    path('contact/', views.contact, name='contact'),
    path('debug/', views.debug, name='debug'),
]
