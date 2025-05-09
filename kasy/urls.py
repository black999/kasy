from django.urls import path
from . import views


urlpatterns = [
     # Home
     path('', views.home, name='home'),

     # Zgloszenie Posnet
     path('zgloszenie_posnet', views.zgloszenie_posnet, name='zgloszenie_posnet'),

     # Kasa
     path('kasa/<int:pk>/edycja', views.kasa_edycja, name='kasa_edycja'),
     path('kasa/lista/<str:typ>', views.kasa_lista, name='kasa_lista'),
     path('kasa/<int:pk>/detale', views.kasa_detale, name='kasa_detale'),
     path('kasa/<int:pk>/zgloszenieUS_podatnik', views.zgloszenieUS_podatnik, name='zgloszenieUS_podatnik'),
     path('kasa/<int:pk>/zgloszenieUS_serwis', views.zgloszenieUS_serwis, name='zgloszenieUS_serwis'),
     path('kasa/<int:pk>/przeglad', views.kasa_przeglad, name='kasa_przeglad'),
     path('kasa/przeglad/ostatnie', views.przeglad_ostatnie, name='przeglad_ostatnie'),
     path('kasa/przeglad/raportUS/<int:rok>/<int:mie>', views.przeglad_raportUS, name='przeglad_raportUS'),
     path('kasa/<int:pk>/sms', views.kasa_sms, name='kasa_sms'),
     path('kasa/<int:pk>/przesun_przeglad', views.kasa_przesun_przeglad, name='kasa_przesun_przeglad'),
     path('kasa/przeglad/<int:rok>/<int:mie>', views.przeglad_rok_miesiac, name='przeglad_rok_miesiac'),
     path('kasa/przeglad/<int:pk>/faktura/<int:rok>/<int:mie>', views.przeglad_faktura, name='przeglad_faktura'),
     path('kasa/szukaj', views.kasa_szukaj, name='kasa_szukaj'),
     path('kasa/<int:pk>/odczyt', views.kasa_odczyt, name='kasa_odczyt'),
     path('kasa/<int:pk>/wyrejUS', views.kasa_wyrejestrowanieUS, name='kasa_wyrejUS'),

     # Odczyt
     path('odczyt/lista', views.odczyt_lista, name='odczyt_lista'),
     path('odczyt/<int:pk>/edycja', views.odczyt_edycja, name='odczyt_edycja'),
     path('odczyt/<int:pk>/zatwierdz', views.odczyt_zatwierdz, name='odczyt_zatwierdz'),
     path('odczyt/<int:pk>/usun', views.odczyt_usun, name='odczyt_usun'),
     path('odczyt/<int:pk>/raportUS', views.odczyt_raportUS, name='odczyt_raportUS'),

     # Podatnik
     path('podatnik/dodaj', views.podatnik_dodaj, name='podatnik_dodaj'),
     path('podatnik/lista', views.podatnik_lista, name='podatnik_lista'),
     path('podatnik/<int:pk>/detale', views.podatnik_detale, name='podatnik_detale'),
     path('podatnik/<int:pk>/edycja', views.podatnik_edycja, name='podatnik_edycja'),
     path('podatnik/<int:pk>/kasa_nowa', views.kasa_dodaj, name='kasa_dodaj'),
]
