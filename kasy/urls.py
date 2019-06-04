from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('kasa/dodaj', views.kasa_dodaj, name='kasa_dodaj'),
    path('kasa/<int:pk>/edycja', views.kasa_edycja, name='kasa_edycja'),
    path('kasa/lista', views.ListaKas.as_view(), name='kasa_lista'),
    path('kasa/<int:pk>/detale', views.kasa_detale, name='kasa_detale'),
    path('kasa/<int:pk>/przeglad', views.kasa_przeglad, name='kasa_przeglad'),
    path('kasa/szukaj', views.kasa_szukaj, name='kasa_szukaj'),
    path('podatnik/dodaj', views.podatnik_dodaj, name='podatnik_dodaj'),
    path('podatnik/lista', views.podatnik_lista, name='podatnik_lista'),
    path('podatnik/<int:pk>/detale', views.podatnik_detale,
         name='podatnik_detale'),
    path('podatnik/<int:pk>/edycja', views.podatnik_edycja,
         name='podatnik_edycja'),
    path('podatnik/<int:pk>/kasa_nowa', views.kasa_dodaj,
         name='kasa_dodaj')
]
