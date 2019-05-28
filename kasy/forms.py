from django import forms
from .models import Kasa, Podatnik, Przeglad
import datetime


class KasaForm(forms.ModelForm):

    class Meta:
        model = Kasa
        # fields = '__all__'
        exclude = ['nastepny_przeg', 'podatnik']
        widgets = {
            'data_fisk': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today() + datetime.timedelta(15)}),
        }


class PodatnikForm(forms.ModelForm):

    class Meta:
        model = Podatnik
        fields = '__all__'


class PrzegladForm(forms.ModelForm):

    class Meta:
        model = Przeglad
        exclude = ['kasa']
        widgets = {
            'data': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today()}),
        }
