from django.db import models


class Producent_kasy(models.Model):
	nazwa 			= models.CharField(max_length=25)		
	ulica 			= models.CharField(max_length=25)
	nr_domu			= models.CharField(max_length=6)
	kod_pocztowy	= models.CharField(max_length=6)
	miasto			= models.CharField(max_length=25)

	def __str__(self):
		return self.nazwa

	class Meta:
		verbose_name_plural = 'Producenci kas'



class Model_kasy(models.Model):
	nazwa			= models.CharField(max_length=20)
	producent 		= models.ForeignKey(Producent_kasy, on_delete=models.CASCADE)

	def __str__(self):
		return self.nazwa

	class Meta:
		verbose_name_plural = 'Modele kas'


class Podatnik(models.Model):
	nazwa			= models.CharField(max_length=30)
	nazwa_cd		= models.CharField(max_length=30)
	kod_pocztowy	= models.CharField(max_length=6)
	miasto			= models.CharField(max_length=25)
	ulica			= models.CharField(max_length=25)
	nr_domu			= models.CharField(max_length=6)
	nip				= models.CharField(max_length=10)
	wojewodzctwo	= models.CharField(max_length=15)
	gmina			= models.CharField(max_length=15)
	poczta			= models.CharField(max_length=25)
	telefon			= models.CharField(max_length=12)


class Serwisant(models.Model):
	nazwisko		= models.CharField(max_length=15)
	imie			= models.CharField(max_length=15)
	nr_plomby		= models.IntegerField()

	def __str__(self):
		return self.nazwisko + ' ' + self.imie

	class Meta:
		verbose_name_plural = 'Serwisanci'


class Urzad_skarbowy(models.Model):
	nazwa 			= models.CharField(max_length=25)
	ulica			= models.CharField(max_length=25)
	nr_domu			= models.CharField(max_length=6)
	kod_pocztowy	= models.CharField(max_length=6)
	miasto			= models.CharField(max_length=25)


class Kasa(models.Model):
	model_kasy		= models.ForeignKey(Model_kasy, on_delete=models.CASCADE)
	nr_unikatowy	= models.CharField(max_length=12)
	nr_fabryczny	= models.CharField(max_length=12)
	urzad_skarbowy 	= models.ForeignKey(Urzad_skarbowy, on_delete=models.CASCADE)
	podatnik 		= models.ForeignKey(Podatnik, on_delete=models.CASCADE)
	data_fisk		= models.DateField()
	ostatni_przeg	= models.DateField()
	cykl_przeg		= models.CharField(max_length=1)


class Przeglad(models.Model):
	kasa 			= models.ForeignKey(Kasa, on_delete=models.CASCADE)
	data 			= models.DateField()


		