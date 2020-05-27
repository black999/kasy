from django.shortcuts import render, redirect, get_object_or_404
import xlwt
from django.http import HttpResponse
from .forms import *
from .models import *
# from django.views.generic.list import ListView
import datetime
# from .tools import Render
from django_xhtml2pdf.utils import generate_pdf


def home(request):
    kasy = Kasa.objects.filter(aktywna=True).order_by('nastepny_przeg')[:20]
    niezgloszone = len(Kasa.objects.filter(zgloszona_do_producenta=False))
    context = {
        'kasy': kasy,
        'niezgloszone': niezgloszone,
        'header': 'Przeglądy'
    }
    return render(request, 'kasy/przeglady_oczekujace.html', context)


# class ListaKas(ListView, pk):
#     template_name = 'kasy/kasa_lista.html'
#     queryset = Kasa.objects.all().select_related('podatnik')
#     model = Kasa
#     context_object_name = 'kasy'

def kasa_lista(request, typ):
    if typ == 'aktywne':
        kasy = Kasa.objects.filter(aktywna=True).filter(
            odczytana=False).select_related('podatnik')
        title = 'Aktywne'
    elif typ == 'nieaktywne':
        kasy = Kasa.objects.filter(aktywna=False).filter(
            odczytana=False).select_related('podatnik')
        title = 'Nieaktywne'
    elif typ == 'odczytane':
        kasy = Kasa.objects.filter(odczytana=True).select_related('podatnik')
        title = 'Odczytane'
    elif typ == 'all':
        kasy = Kasa.objects.all().select_related('podatnik')
        title = 'Wszystkie'
    context = {
        'kasy': kasy,
        'title': title,
        'header': 'Urządzenia fiskalne'
    }
    return render(request, 'kasy/kasa_lista.html', context)


def kasa_szukaj(request):
    if request.method == 'POST':
        kasy = Kasa.objects.filter(
            nr_unikatowy__contains=request.POST['nr_unikatowy'])
        return render(request, 'kasy/kasa_lista.html', {'kasy': kasy})
    else:
        return redirect('home')


def kasa_dodaj(request, pk):
    # pk - id podatnika
    if request.method == 'POST':
        form = KasaForm(request.POST)
        if form.is_valid():
            kasa = form.save(commit=False)
            kasa.model_kasy_id = request.POST['model_kasy']
            kasa.podatnik_id = pk
            kasa.nastepny_przeglad(kasa.data_fisk)
            kasa.save()
            return redirect('podatnik_detale', pk=pk)
    else:
        form = KasaForm()
    podatnik = get_object_or_404(Podatnik, pk=pk)
    context = {
        'form': form,
        'podatnik': podatnik,
        'header': 'Urządzenia',
        'title': 'Nowa kasa/drukarka fiskalna'
    }
    return render(request, 'kasy/kasa_edycja.html', context)


def kasa_edycja(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    if request.method == 'POST':
        form = KasaForm(request.POST, instance=kasa)
        if form.is_valid():
            kasa = form.save(commit=False)
            ostatni_przeglad = Przeglad.objects.filter(
                kasa=pk).order_by('-data')
            if ostatni_przeglad.count() > 0:
                kasa.nastepny_przeglad(ostatni_przeglad[0].data)
            else:
                kasa.nastepny_przeglad(kasa.data_fisk)
            kasa.save()
            return redirect('kasa_detale', pk=pk)
    else:
        kasa.data_fisk = kasa.data_fisk.strftime('%Y-%m-%d')
        form = KasaForm(instance=kasa)
    podatnik = get_object_or_404(Podatnik, pk=kasa.podatnik.pk)
    context = {
        'podatnik': podatnik,
        'form': form,
        'header': 'Urządzenia',
        'title': 'Edycja kasy/drukarki fiskalnej'
    }
    return render(request, 'kasy/kasa_edycja.html', context)


def kasa_detale(request, pk):
    form = PrzegladForm()
    kasa = get_object_or_404(Kasa, pk=pk)
    odczyt = Odczyt.objects.filter(kasa__pk=pk)
    if len(odczyt) > 0:
        odczyt = odczyt[0]
    else:
        odczyt = False
    przeglady = Przeglad.objects.filter(kasa=pk).order_by('-data')
    context = { 
      'kasa': kasa,
      'form': form,
      'przeglady': przeglady,
      'odczyt': odczyt,
      'header': 'Szczegóły urządzenia'
    }
    return render(request, 'kasy/kasa_detale.html', context)



def kasa_przeglad(request, pk):
    if request.method == 'POST':
        form = PrzegladForm(request.POST)
        if form.is_valid():
            przeglad = form.save(commit=False)
            kasa = Kasa.objects.get(pk=pk)
            kasa.nastepny_przeglad(przeglad.data)
            kasa.sms = False
            kasa.save()
            przeglad.kasa = kasa
            przeglad.save()
            return redirect('kasa_detale', pk=pk)


def kasa_sms(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    kasa.sms = True
    kasa.data_sms = datetime.datetime.now()
    kasa.save()
    return redirect('home')


def kasa_przesun_przeglad(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    kasa.przesun_przeglad()
    kasa.sms = False
    kasa.save()
    return redirect('home')


def kasa_odczyt(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    if request.method == 'POST':
        form = OdczytForm(request.POST)
        if form.is_valid:
            odczyt = form.save(commit=False)
            odczyt.kasa = kasa
            odczyt.serwisant_id = request.POST['serwisant']
            odczyt.save()
            kasa.odczytaj()
            kasa.aktywna = False
            kasa.save()
            return redirect('odczyt_lista')
    else:
        form = OdczytForm()
    context = {
        'form': form,
        'kasa': kasa,
        'header': 'Odczyty'
    }
    return render(request, 'kasy/kasa_odczyt.html', context)


def kasa_wyrejestrowanieUS(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    podatnik = kasa.podatnik
    return render(request, 'kasy/kasa_wyrejestrowanieUS.html',
                  {'kasa': kasa,
                   'podatnik': podatnik})


def kasa_do_wymiany(request):
    kasy = Kasa.objects.filter(przeglad__ilosc_raportow__gt=1400).filter(aktywna=
        True).distinct()
    context = {
        'kasy' : kasy,
        'header': 'Kasy do wymiany'
    }
    return render(request, 'kasy/kasa_do_wymiany.html', context)


def zgloszenieUS_podatnik(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    podatnik = kasa.podatnik
    context = {
        'podatnik': podatnik,
        'kasa': kasa
    }
    return render(request, 'kasy/zgloszenieUS_podatnik.html', context)


def zgloszenieUS_serwis(request, pk):
    kasa = get_object_or_404(Kasa, pk=pk)
    podatnik = kasa.podatnik
    context = {
        'podatnik': podatnik,
        'kasa': kasa
    }
    return render(request, 'kasy/zgloszenieUS_serwis.html', context)


def odczyt_lista(request):
    odczyty = Odczyt.objects.all()
    context = {
        'odczyty': odczyty,
        'header': 'Odczyty'
    }
    return render(request, 'kasy/odczyt_lista.html', context)


def odczyt_edycja(request, pk):
    odczyt = get_object_or_404(Odczyt, pk=pk)
    if request.method == 'POST':
        form = OdczytForm(request.POST, instance=odczyt)
        if form.is_valid:
            form.save()
            return redirect('odczyt_lista')
    else:
        odczyt.data = odczyt.data.strftime('%Y-%m-%d')
        odczyt.od_daty = odczyt.od_daty.strftime('%Y-%m-%d')
        odczyt.do_daty = odczyt.do_daty.strftime('%Y-%m-%d')
        form = OdczytForm(instance=odczyt)
    return render(request, 'kasy/kasa_odczyt.html',
                  {'form': form, 'kasa': odczyt.kasa})


def odczyt_zatwierdz(request, pk):
    odczyt = get_object_or_404(Odczyt, pk=pk)
    odczyt.zatwierdz()
    odczyt.save()
    form = PrzegladForm()
    kasa = Kasa.objects.get(id=odczyt.kasa.id)
    przeglady = Przeglad.objects.filter(kasa=kasa.pk).order_by('-data')
    context =  {
      'kasa': kasa,
      'form': form,
      'przeglady': przeglady,
      'odczyt': odczyt
    }
    return render(request, 'kasy/kasa_detale.html', context)


def odczyt_usun(request, pk):
    odczyt = get_object_or_404(Odczyt, pk=pk)
    if not odczyt.zatwierdzony:
        odczyt.kasa.odczytana = False
        odczyt.kasa.save()
        odczyt.delete()
    return redirect('odczyt_lista')

def odczyt_raportUS(request, pk):
    odczyt = get_object_or_404(Odczyt, pk=pk)
    kasa = odczyt.kasa
    podatnik = kasa.podatnik
    context = {'odczyt': odczyt, 'kasa': kasa, 'podatnik': podatnik}
    #return render(request, 'kasy/odczyt_raportUS.html', context)
    #return Render.render('kasy/odczyt_raportUS.html', context)
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="dokument.pdf"'
    result = generate_pdf('kasy/odczyt_raportUS.html', file_object=response, context=context)
    return result


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
    context = {
        'podatnicy': podatnicy,
        'header': 'Firmy'
    }
    return render(request, 'kasy/podatnik_lista.html', context)


def podatnik_detale(request, pk):
    kasy = Kasa.objects.filter(podatnik=pk)
    podatnik = get_object_or_404(Podatnik, pk=pk)
    context = {
        'podatnik': podatnik,
        'kasy': kasy,
        'header': 'Firma szczegóły'
    }
    return render(request, 'kasy/podatnik_detale.html', context)


def podatnik_edycja(request, pk):
    podatnik = get_object_or_404(Podatnik, pk=pk)
    if request.method == 'POST':
        form = PodatnikForm(request.POST, instance=podatnik)
        if form.is_valid():
            form.save()
            return redirect('podatnik_detale', pk=pk)
    else:
        form = PodatnikForm(instance=podatnik)
    return render(request, 'kasy/podatnik_edycja.html', {'form': form})


def przeglad_ostatnie(request):
    data = datetime.date.today()
    form = PrzegladRokMiesiac({'rok': data.year, 'mie': data.month})
    print(form.data['rok'])
    przeglady = Przeglad.objects.filter(
        data__year=data.year, data__month=data.month)
    context = {
        'przeglady': przeglady,
        'form': form,
        'data': data,
        'header': 'Przeglądy'
    }
    return render(request,'kasy/przeglad_ostatnie.html', context)


def przeglad_rok_miesiac(request, rok, mie):
    if request.method == 'POST':
        return redirect('przeglad_rok_miesiac',
                        rok=request.POST['rok'], mie=request.POST['mie'])
    else:
        data = datetime.date.today()
        form = PrzegladRokMiesiac({'rok': rok, 'mie': mie})
        if mie == 0:
            przeglady = Przeglad.objects.filter(
                data__year=rok).order_by('data')
        else:
            przeglady = Przeglad.objects.filter(
                data__year=rok, data__month=mie).order_by('data')
        return render(request,
                      'kasy/przeglad_ostatnie.html',
                      {'przeglady': przeglady, 'form': form, 'data': data})


def przeglad_faktura(request, pk, rok, mie):
    przeglad = get_object_or_404(Przeglad, pk=pk)
    przeglad.wystaw_fakture()
    przeglad.save()
    return redirect('przeglad_rok_miesiac', rok=rok, mie=mie)


def przeglad_raportUS(request, rok, mie):
    if mie == 0:
        urzedy = Urzad_skarbowy.objects.filter(
            podatnik__kasa__przeglad__data__year=rok).distinct()
        przeglady = Przeglad.objects.filter(
            data__year=rok).order_by('data')
    else:
        urzedy = Urzad_skarbowy.objects.filter(
            podatnik__kasa__przeglad__data__year=rok,
            podatnik__kasa__przeglad__data__month=mie).distinct()
        przeglady = Przeglad.objects.filter(
            data__year=rok, data__month=mie).order_by(
            'data')
    return render(request, 'kasy/przeglad_raportUS.html',
                  {'przeglady': przeglady,
                   'urzedy': urzedy, 'rok': rok, 'mie': mie})


def zgloszenie_posnet(request):
    response = HttpResponse(content_type='application/ms-excel')
    attachment = "attachment; filename=fiskalizacje" \
        + str(datetime.date.today()) + ".xls"
    # response['Content-Disposition'] = 'attachment; filename=filename'
    response['Content-Disposition'] = attachment
    kasy = Kasa.objects.filter(
        zgloszona_do_producenta=False).order_by('data_fisk')

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

    font_style = xlwt.XFStyle()
    row_num = 0
    # col_num = 0

    for kasa in kasy:
        ws.write(row_num, 0, str(kasa.nr_fabryczny), font_style)
        ws.write(row_num, 1, str(kasa.nr_unikatowy), font_style)
        ws.write(row_num, 2, str(kasa.data_fisk), font_style)
        ws.write(row_num, 3, str(kasa.podatnik.nip), font_style)
        ws.write(row_num, 4, str(kasa.podatnik), font_style)
        ws.write(row_num, 5, str(kasa.podatnik.kod_pocztowy), font_style)
        ws.write(row_num, 6, str(kasa.podatnik.poczta), font_style)
        ws.write(row_num, 7, str(kasa.podatnik.miasto), font_style)
        ws.write(row_num, 8, str(kasa.podatnik.ulica), font_style)
        ws.write(row_num, 9, str(kasa.podatnik.nr_domu), font_style)
        ws.write(row_num, 10, "", font_style)
        ws.write(row_num, 11, str(kasa.podatnik.telefon), font_style)
        ws.write(row_num, 12, str(kasa.podatnik.email), font_style)
        ws.write(row_num, 13, str(kasa.podatnik.email), font_style)
        ws.write(row_num, 14, "0", font_style)
        ws.write(row_num, 15, "", font_style)
        ws.write(row_num, 16, "", font_style)
        ws.write(row_num, 17, "", font_style)
        ws.write(row_num, 18, "", font_style)
        ws.write(row_num, 19, "", font_style)
        ws.write(row_num, 20, "", font_style)
        ws.write(row_num, 21, "", font_style)
        ws.write(row_num, 22, str(
            kasa.podatnik.urzad_skarbowy.nr_urzedu), font_style)
        ws.write(row_num, 23, str(kasa.nr_nadany), font_style)
        row_num += 1
        kasa.zglos_do_posnet()
        kasa.save()

    wb.save(response)

    return response
