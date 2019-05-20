from django.contrib import admin
from .models import Producent_kasy, Model_kasy, Serwisant, Urzad_skarbowy, Kasa


admin.site.register(Producent_kasy)
admin.site.register(Model_kasy)
admin.site.register(Serwisant)
admin.site.register(Urzad_skarbowy)
admin.site.register(Kasa)

