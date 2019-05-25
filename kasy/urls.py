from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('kasa/dodaj', views.nowa_kasa, name='nowa_kasa'),
    path('kasa/<int:pk>/edycja', views.kasa_edycja, name='kasa_edycja'),
    path('kasa/lista', views.ListaKas.as_view(), name='lista_kas'),
    path('podatnik/dodaj', views.nowy_podatnik, name='nowy_podatnik'),
    path('podatenik/lista', views.lista_podatnik, name='lista_podatnik')

]
