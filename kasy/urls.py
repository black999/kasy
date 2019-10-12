from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    # path('kasa/dodaj', views.kasa_dodaj, name='kasa_dodaj'),
    path('kasa/<int:pk>/edycja', views.kasa_edycja, name='kasa_edycja'),
    path('kasa/lista/<str:typ>', views.kasa_lista, name='kasa_lista'),
    path('kasa/<int:pk>/detale', views.kasa_detale, name='kasa_detale'),
    path('kasa/<int:pk>/przeglad', views.kasa_przeglad, name='kasa_przeglad'),
    path('kasa/<int:pk>/odczyt', views.kasa_odczyt, name='kasa_odczyt'),
    path('kasa/przeglad/ostatnie', views.przeglad_ostatnie,
         name='przeglad_ostatnie'),
    path('kasa/przeglad/<int:rok>/<int:mie>',
         views.przeglad_rok_miesiac, name='przeglad_rok_miesiac'),
    path('kasa/przeglad/<int:pk>/faktura/<int:rok>/<int:mie>',
         views.przeglad_faktura, name='przeglad_faktura'),
    path('kasa/przeglad/raportUS/<int:rok>/<int:mie>',
         views.przeglad_raportUS, name='przeglad_raportUS'),
    path('kasa/szukaj', views.kasa_szukaj, name='kasa_szukaj'),
    path('kasa/odczyt', views.odczyt_lista, name='odczyt_lista'),
    path('kasa/odczyt/<int:pk>/edycja',
         views.odczyt_edycja, name='odczyt_edycja'),
    path('podatnik/dodaj', views.podatnik_dodaj, name='podatnik_dodaj'),
    path('podatnik/lista', views.podatnik_lista, name='podatnik_lista'),
    path('podatnik/<int:pk>/detale', views.podatnik_detale,
         name='podatnik_detale'),
    path('podatnik/<int:pk>/edycja', views.podatnik_edycja,
         name='podatnik_edycja'),
    path('podatnik/<int:pk>/kasa_nowa', views.kasa_dodaj,
         name='kasa_dodaj')
]
