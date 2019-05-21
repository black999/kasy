from django.shortcuts import render, redirect
from .forms import KasaForm, PodatnikForm
from django.utils import timezone
from .models import Model_kasy, Urzad_skarbowy, Podatnik


def home(request):
    return render(request, 'kasy/base.html')


def nowa_kasa(request):
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid:
            kasa = form.save(commit=False)
            kasa.model_kasy = Model_kasy.objects.get(
                pk=request.POST['model_kasy'])
            kasa.urzad_skarbowy = Urzad_skarbowy.objects.get(
                pk=request.POST['urzad_skarbowy'])
            kasa.podatnik = Podatnik.objects.get(pk=request.POST['podatnik'])
            # kasa.data_fisk = timezone.now()
            # kasa.ostatni_przeg = timezone.now()
            kasa.save()
            return redirect('home')
    else:
        form = KasaForm()
    return render(request, 'kasy/nowa_kasa.html', {'form': form})


def nowy_podatnik(request):
    if request.method == 'POST':
        form = PodatnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PodatnikForm()
    return render(request, 'kasy/nowy_podatnik.html', {'form': form})
