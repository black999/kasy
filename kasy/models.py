from django.db import models
import datetime

PRZEGLAD = [
    ('1', 'Roczny'),
    ('2', 'Dwuletni')
]


class Producent_kasy(models.Model):
    nazwa = models.CharField(max_length=40)
    ulica = models.CharField(max_length=25)
    nr_domu = models.CharField(max_length=6)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=25)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Producenci kas'


class Model_kasy(models.Model):
    nazwa = models.CharField(max_length=20)
    producent = models.ForeignKey(Producent_kasy, on_delete=models.CASCADE)

    def __str__(self):
        return self.nazwa

    class Meta:
        verbose_name_plural = 'Modele kas'


class Urzad_skarbowy(models.Model):
    nazwa = models.CharField(max_length=25)
    ulica = models.CharField(max_length=25)
    nr_domu = models.CharField(max_length=6)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=25)

    def __str__(self):
        return self.nazwa + " " + self.miasto

    class Meta:
        verbose_name_plural = "Urzędy Skarbowe"


class Podatnik(models.Model):
    nazwa = models.CharField(max_length=30)
    nazwa_cd = models.CharField(max_length=30, blank=True, null=True)
    kod_pocztowy = models.CharField(max_length=6)
    miasto = models.CharField(max_length=25)
    ulica = models.CharField(max_length=25)
    nr_domu = models.CharField(max_length=6)
    nip = models.CharField(max_length=10, unique=True)
    wojewodzctwo = models.CharField(max_length=15)
    gmina = models.CharField(max_length=15)
    poczta = models.CharField(max_length=25)
    telefon = models.CharField(max_length=12)
    email = models.Charfield(max_length=50, blank=True, null=True)
    urzad_skarbowy = models.ForeignKey(
        Urzad_skarbowy, on_delete=models.CASCADE)

    def __str__(self):
        if self.nazwa_cd:
            return self.nazwa + " " + self.nazwa_cd
        else:
            return self.nazwa 


class Serwisant(models.Model):
    nazwisko = models.CharField(max_length=15)
    imie = models.CharField(max_length=15)
    nr_plomby = models.IntegerField()

    def __str__(self):
        return self.nazwisko + ' ' + self.imie

    class Meta:
        verbose_name_plural = 'Serwisanci'


class Kasa(models.Model):
    model_kasy = models.ForeignKey(Model_kasy, on_delete=models.CASCADE)
    nr_unikatowy = models.CharField(max_length=13, unique=True)
    nr_fabryczny = models.CharField(max_length=11)
    nr_nadany = models.CharField(max_length=15,blank=True, null=True)
    podatnik = models.ForeignKey(Podatnik, on_delete=models.CASCADE)
    miejsce_inst = models.CharField(max_length=60, default='siedziba firmy')
    data_fisk = models.DateField()
    nastepny_przeg = models.DateField(blank=True, null=True)
    cykl_przeg = models.CharField(max_length=10, choices=PRZEGLAD, default='1')

    def __str__(self):
        return self.model_kasy.nazwa

    def nastepny_przeglad(self, data):
        if self.cykl_przeg == '1':
            self.nastepny_przeg = data + datetime.timedelta(360)
        else:
            self.nastepny_przeg = data + datetime.timedelta(720)


class Przeglad(models.Model):
    kasa = models.ForeignKey(Kasa, on_delete=models.CASCADE)
    serwisant = models.ForeignKey(Serwisant, on_delete=models.CASCADE)
    data = models.DateField(default=0)
    ilosc_raportow = models.IntegerField()
    info = models.CharField(max_length=60, blank=True, null=True)
