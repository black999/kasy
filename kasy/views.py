from django.shortcuts import render, redirect, get_object_or_404
from .forms import KasaForm, PodatnikForm, PrzegladForm
from .models import Model_kasy, Urzad_skarbowy, Podatnik, Kasa, Przeglad
from django.views.generic.list import ListView
import datetime


def home(request):
    kasy = Kasa.objects.order_by('nastepny_przeg')[:10]
    return render(request, 'kasy/przeglady_oczekujace.html', {'kasy': kasy})


class ListaKas(ListView):
    template_name = 'kasy/kasa_lista.html'
    # queryset = Kasa.objects.all()
    model = Kasa
    context_object_name = 'kasy'

def kasa_szukaj(request, nr_unikatowy):
    kasy = Kasa.objects.filter(nr_unikatowy__contains=nr_unikatowy) 
    return render(request, 'kasy/kasa_lista.html', {'kasy': kasy})

def kasa_dodaj(request, pk):
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid():
            kasa = form.save(commit=False)
            kasa.model_kasy = Model_kasy.objects.get(
                pk=request.POST['model_kasy'])
            kasa.podatnik = Podatnik.objects.get(pk=pk)
            kasa.nastepny_przeglad(kasa.data_fisk)
            kasa.save()
            return redirect('podatnik_detale', pk=pk)
    else:
        form = KasaForm()
    return render(request, 'kasy/kasa_edycja.html', {'form': form})


def kasa_edycja(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    form = KasaForm(instance=kasa)
    return render(request, 'kasy/kasa_edycja.html', {'form': form})


def kasa_detale(request, pk):
    form = PrzegladForm()
    kasa = get_object_or_404(Kasa, pk=pk)
    przeglady = Przeglad.objects.filter(kasa=pk)
    return render(request, 'kasy/kasa_detale.html',
                  {'kasa': kasa, 'form': form, 'przeglady': przeglady})


def kasa_przeglad(request, pk):
    if request.method == 'POST':
        form = PrzegladForm(request.POST)
        if form.is_valid():
            przeglad = form.save(commit=False)
            kasa = Kasa.objects.get(pk=pk)
            kasa.nastepny_przeglad(przeglad.data)
            kasa.save()
            przeglad.kasa = kasa
            przeglad.save()
            return redirect('kasa_detale', pk=pk)


def podatnik_dodaj(request):
    if request.method == 'POST':
        form = PodatnikForm(request.POST)
        if form.is_valid():
            podatnik = form.save(commit=False)
            podatnik.save()
            return redirect('podatnik_detale', pk=podatnik.pk)
    else:
        form = PodatnikForm()
    return render(request, 'kasy/podatnik_edycja.html', {'form': form})


def podatnik_lista(request):
    podatnicy = Podatnik.objects.all()
    return render(request, 'kasy/podatnik_lista.html',
                  {'podatnicy': podatnicy})


def podatnik_detale(request, pk):
    kasy = Kasa.objects.filter(podatnik=pk)
    podatnik = get_object_or_404(Podatnik, pk=pk)
    return render(request, 'kasy/podatnik_detale.html',
                  {'podatnik': podatnik, 'kasy': kasy})


def podatnik_edycja(request, pk):
    podatnik = get_object_or_404(Podatnik, pk=pk)
    form = PodatnikForm(instance=podatnik)
    return render(request, 'kasy/podatnik_edycja.html', {'form': form})
