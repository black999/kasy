from django import forms
from .models import Kasa, Podatnik


class KasaForm(forms.ModelForm):

    class Meta:
        model = Kasa
        fields = '__all__'


class PodatnikForm(forms.ModelForm):

    class Meta:
        model = Podatnik
        fields = '__all__'
