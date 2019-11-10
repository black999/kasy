from django import forms
from .models import Kasa, Podatnik, Przeglad, Odczyt
import datetime


class KasaForm(forms.ModelForm):

    class Meta:
        model = Kasa
        # fields = '__all__'
        exclude = [
            'nastepny_przeg',
            'podatnik',
            'odczytana',
            'sms',
            'data_sms',
            'zgloszona_do_producenta'
        ]
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
        exclude = ['kasa', 'faktura']
        widgets = {
            'data': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today()}),
        }


class PrzegladRokMiesiac(forms.Form):
    rok_biezacy = datetime.date.today().year
    mie_biezacy = datetime.date.today().month
    lata = [('2018', '2018'), ('2019', '2019'),
            ('2020', '2020'), ('2021', '2021')]
    miesiace = [('0', 'cały rok'), ('1', 'styczeń'), ('2', 'luty'),
                ('3', 'marzec'), ('4', 'kwiecień'),
                ('5', 'maj'), ('6', 'czerwiec'),
                ('7', 'lipiec'), ('8', 'sierpien'),
                ('9', 'wrzesień'), ('10', 'październik'),
                ('11', 'listopad'), ('12', 'grudzień')]
    rok = forms.ChoiceField(label='', choices=lata,
                            initial=rok_biezacy, widget=forms.Select())
    mie = forms.ChoiceField(label='', choices=miesiace,
                            initial=mie_biezacy, widget=forms.Select())


class OdczytForm(forms.ModelForm):

    class Meta:
        model = Odczyt
        exclude = ['kasa']
        widgets = {
            'data': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today()}),
            'od_daty': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today()}),
            'do_daty': forms.widgets.DateInput(
                attrs={'type': 'date',
                       'max': datetime.date.today()}),
            'sp_ptu_a1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_b1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_c1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_d1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_e1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_f1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_g1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_a2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_b2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_c2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_d2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_e2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_f2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'sp_ptu_g2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_a1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_b1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_c1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_d1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_e1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_f1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_g1': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_a2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_b2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_c2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_d2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_e2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_f2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
            'ptu_g2': forms.widgets.NumberInput(
                attrs={'max': 99999999.99}),
        }
