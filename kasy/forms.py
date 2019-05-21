from django import forms
from .models import Kasa, Podatnik
import datetime


class KasaForm(forms.ModelForm):

    class Meta:
        model = Kasa
        # fields = '__all__'
        exclude = ['ostatni_przeg']
        widgets = {
            'data_fisk': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today() + datetime.timedelta(15)}),
        }


class PodatnikForm(forms.ModelForm):

    class Meta:
        model = Podatnik
        fields = '__all__'
