from django import forms
from .models import Kasa, Podatnik


class DateInput(forms.DateInput):
	input_type = 'date'

class KasaForm(forms.ModelForm):

    class Meta:
        model = Kasa
        fields = '__all__'
        widgets = {
        	'data_fisk' : DateInput(),
        	'ostatni_przeg' : DateInput(),
        }


class PodatnikForm(forms.ModelForm):

    class Meta:
        model = Podatnik
        fields = '__all__'
