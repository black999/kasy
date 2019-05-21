from django import forms
from .models import Kasa, Podatnik


class KasaForm(forms.ModelForm):

    class Meta:
        model = Kasa
        # fields = '__all__'
        exclude = ['ostatni_przeg']
        widgets = {
        	'data_fisk' : forms.widgets.DateInput(attrs={'type' : 'date'}),
        	'ostatni_przeg' : forms.widgets.DateInput(attrs={'type' : 'date'}),
        }



class PodatnikForm(forms.ModelForm):

    class Meta:
        model = Podatnik
        fields = '__all__'
