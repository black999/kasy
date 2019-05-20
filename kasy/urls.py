from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('kasa/dodaj', views.nowa_kasa, name='nowa_kasa'),
    path('podatnik/dodaj', views.nowy_podatnik, name='nowy_podatnik')
]
