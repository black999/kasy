from django.shortcuts import render, redirect, get_object_or_404
from .forms import KasaForm, PodatnikForm
from .models import Model_kasy, Urzad_skarbowy, Podatnik, Kasa
from django.views.generic.list import ListView


def home(request):
    return render(request, 'kasy/base.html')


class ListaKas(ListView):
    template_name = 'kasy/lista_kas.html'
    # queryset = Kasa.objects.all()
    model = Kasa
    context_object_name = 'kasy'


def nowa_kasa(request):
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid():
            kasa = form.save(commit=False)
            kasa.model_kasy = Model_kasy.objects.get(
                pk=request.POST['model_kasy'])
            kasa.urzad_skarbowy = Urzad_skarbowy.objects.get(
                pk=request.POST['urzad_skarbowy'])
            kasa.podatnik = Podatnik.objects.get(pk=request.POST['podatnik'])
            kasa.save()
            return redirect('home')
    else:
        form = KasaForm()
    return render(request, 'kasy/kasa_edycja.html', {'form': form})


def kasa_edycja(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    form = KasaForm(instance=kasa)
    return render(request, 'kasy/kasa_edycja.html', {'form': form})


def nowy_podatnik(request):
    if request.method == 'POST':
        form = PodatnikForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PodatnikForm()
    return render(request, 'kasy/nowy_podatnik.html', {'form': form})
