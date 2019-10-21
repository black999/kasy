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
    nr_urzedu = models.PositiveSmallIntegerField()

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
    nip = models.CharField(max_length=13, unique=True)
    wojewodzctwo = models.CharField(max_length=15)
    gmina = models.CharField(max_length=15)
    poczta = models.CharField(max_length=25)
    telefon = models.CharField(max_length=12)
    email = models.CharField(max_length=50, blank=True, null=True)
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
    uprawnienia_od = models.DateField()

    def __str__(self):
        return self.nazwisko + ' ' + self.imie

    class Meta:
        verbose_name_plural = 'Serwisanci'


class Kasa(models.Model):
    model_kasy = models.ForeignKey(Model_kasy, on_delete=models.CASCADE)
    nr_unikatowy = models.CharField(max_length=13, unique=True)
    nr_fabryczny = models.CharField(max_length=11)
    nr_nadany = models.CharField(max_length=15, blank=True, null=True)
    podatnik = models.ForeignKey(Podatnik, on_delete=models.CASCADE)
    miejsce_inst = models.CharField(max_length=60, default='siedziba firmy')
    data_fisk = models.DateField()
    nastepny_przeg = models.DateField(blank=True, null=True)
    cykl_przeg = models.CharField(max_length=10, choices=PRZEGLAD, default='1')
    aktywna = models.BooleanField(default=True)
    odczytana = models.BooleanField(default=False)
    sms = models.BooleanField(default=False)
    data_sms = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.model_kasy.nazwa

    def nastepny_przeglad(self, data):
        if self.cykl_przeg == '1':
            self.nastepny_przeg = data + datetime.timedelta(360)
        else:
            self.nastepny_przeg = data + datetime.timedelta(720)

    def przesun_przeglad(self):
        self.nastepny_przeg += datetime.timedelta(31)

    def odczytaj(self):
        self.odczytana = True


class Przeglad(models.Model):
    kasa = models.ForeignKey(Kasa, on_delete=models.CASCADE)
    serwisant = models.ForeignKey(Serwisant, on_delete=models.CASCADE)
    data = models.DateField(default=0)
    ilosc_raportow = models.PositiveSmallIntegerField()
    info = models.CharField(max_length=60, blank=True, null=True)
    faktura = models.BooleanField(default=False)

    def wystaw_fakture(self):
        self.faktura = True


class Odczyt(models.Model):
    kasa = models.ForeignKey(Kasa, on_delete=models.CASCADE)
    serwisant = models.ForeignKey(Serwisant, on_delete=models.CASCADE)
    data = models.DateField("Data odczytu", default=0)
    od_raportu = models.PositiveSmallIntegerField("Od raportu", default=1)
    od_daty = models.DateField("Od daty")
    do_raportu = models.PositiveSmallIntegerField("Do raportu")
    do_daty = models.DateField("Do daty")
    sp_ptu_a1 = models.DecimalField(
        "Sprzedaż PTU A (23%)", max_digits=10, decimal_places=2)
    sp_ptu_b1 = models.DecimalField(
        "Sprzedaż PTU B (8%)", max_digits=10, decimal_places=2)
    sp_ptu_c1 = models.DecimalField(
        "Sprzedaż PTU C (0%)", max_digits=10, decimal_places=2)
    sp_ptu_d1 = models.DecimalField(
        "Sprzedaż PTU D (5%)", max_digits=10, decimal_places=2)
    sp_ptu_e1 = models.DecimalField(
        "Sprzedaż PTU E (..%)", max_digits=10, decimal_places=2)
    sp_ptu_f1 = models.DecimalField(
        "Sprzedaż PTU F (..%)", max_digits=10, decimal_places=2)
    sp_ptu_g1 = models.DecimalField(
        "Sprzedaż PTU G (zw)", max_digits=10, decimal_places=2)
    ptu_a1 = models.DecimalField(
        "Wartość PTU A", max_digits=10, decimal_places=2)
    ptu_b1 = models.DecimalField(
        "Wartość PTU B", max_digits=10, decimal_places=2)
    ptu_c1 = models.DecimalField(
        "Wartość PTU C", max_digits=10, decimal_places=2)
    ptu_d1 = models.DecimalField(
        "Wartość PTU D", max_digits=10, decimal_places=2)
    ptu_e1 = models.DecimalField(
        "Wartość PTU E", max_digits=10, decimal_places=2)
    ptu_f1 = models.DecimalField(
        "Wartość PTU F", max_digits=10, decimal_places=2)
    ptu_g1 = models.DecimalField(
        "Wartość PTU G", max_digits=10, decimal_places=2)
    sp_ptu_a2 = models.DecimalField(
        "Sprzedaż PTU A' (23%)", max_digits=10, decimal_places=2)
    sp_ptu_b2 = models.DecimalField(
        "Sprzedaż PTU B' (8%)", max_digits=10, decimal_places=2)
    sp_ptu_c2 = models.DecimalField(
        "Sprzedaż PTU C' (5%)", max_digits=10, decimal_places=2)
    sp_ptu_d2 = models.DecimalField(
        "Sprzedaż PTU D' (0%)", max_digits=10, decimal_places=2)
    sp_ptu_e2 = models.DecimalField(
        "Sprzedaż PTU E' (zw)", max_digits=10, decimal_places=2)
    sp_ptu_f2 = models.DecimalField(
        "Sprzedaż PTU F' (..%)", max_digits=10, decimal_places=2)
    sp_ptu_g2 = models.DecimalField(
        "Sprzedaż PTU G' (..%)", max_digits=10, decimal_places=2)
    ptu_a2 = models.DecimalField(
        "Wartość PTU A'", max_digits=10, decimal_places=2)
    ptu_b2 = models.DecimalField(
        "Wartość PTU B'", max_digits=10, decimal_places=2)
    ptu_c2 = models.DecimalField(
        "Wartość PTU C'", max_digits=10, decimal_places=2)
    ptu_d2 = models.DecimalField(
        "Wartość PTU D'", max_digits=10, decimal_places=2)
    ptu_e2 = models.DecimalField(
        "Wartość PTU E'", max_digits=10, decimal_places=2)
    ptu_f2 = models.DecimalField(
        "Wartość PTU F'", max_digits=10, decimal_places=2)
    ptu_g2 = models.DecimalField(
        "Wartość PTU G'", max_digits=10, decimal_places=2)
    laczna_sprzedaz_PTU = models.DecimalField(
        "Łączna kwota PTU", max_digits=10, decimal_places=2)
    laczna_wysokosc_PTU = models.DecimalField(
        "Łączna należność", max_digits=10, decimal_places=2)
    liczba_zerowan = models.PositiveSmallIntegerField(
        "Liczba zerowań", default=0)
    liczba_paragonow = models.PositiveSmallIntegerField("Liczba paragonów")
    liczba_faktur = models.PositiveSmallIntegerField(
        "Liczba faktur", default=0)
    liczba_paragonow_anulowanych = models.PositiveSmallIntegerField(
        "Liczba paragonów anulowanych")
    wartosc_paragonow_anulowanych = models.DecimalField(
        "Wartość paragonów anulowanych",
        max_digits=10, decimal_places=2)
    liczba_faktur_anulowanych = models.PositiveSmallIntegerField(
        "Liczba faktur anulowanych", default=0)
    wartosc_faktur_anulowanych = models.DecimalField(
        "Wartość faktur anulowanych",
        max_digits=10, decimal_places=2, default=0)
    daty_przegladow = models.CharField("Daty przeglądów", max_length=100)
    zatwierdzony = models.BooleanField(default=False)

    def zatwierdz(self):
        self.zatwierdzony = True


class config(models.Model):
    sms_access_token = models.CharField("Token SMS", max_length=100)

        