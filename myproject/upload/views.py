from django.shortcuts import render,redirect
from .models import Documents
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib import messages
import os
from django.views.decorators.cache import never_cache

# Create your views here.

#is_files_uploaded = {'calisma_ruhsati':False,'faaliyet_belgesi':False,'imza_sirkuleri':False,'oda_kayit_belgesi':False,'kurulus_sozlesmesi':False,'sirketin_mali_bilgileri':False,'ticaret_sicil_odasi':False,'ticaret_sicil_tasdiknamesi':False,'vergi_levhasi':False,'yetki_belgesi':False}



def home(request):
    
    return render(request, 'upload/home.html')

def documents(request):
    document = Documents.objects.filter(email=request.user).first()
    if not document:
       document = Documents(email=request.user)
       document.save()

    is_files_uploaded = {
    'calisma_ruhsati': bool(document.Calisma_ruhsati_izinler and document.Calisma_ruhsati_izinler.name), 
    'faaliyet_belgesi': bool(document.Faaliyet_belgesi and document.Faaliyet_belgesi.name),
    'imza_sirkuleri': bool(document.Imza_sirkuleri and document.Imza_sirkuleri.name),
    'oda_kayit_belgesi': bool(document.Oda_kayit_belgesi and document.Oda_kayit_belgesi.name),
    'kurulus_sozlesmesi': bool(document.Kurulus_sozlemesi and document.Kurulus_sozlemesi.name),
    'sirketin_mali_bilgileri': bool(document.Sirketin_mali_bilgileri and document.Sirketin_mali_bilgileri.name),
    'ticaret_sicil_odasi': bool(document.Ticaret_sicil_gazetesi and document.Ticaret_sicil_gazetesi.name),
    'ticaret_sicil_tasdiknamesi': bool(document.Ticaret_sicil_tasdiknamesi and document.Ticaret_sicil_tasdiknamesi.name),
    'vergi_levhasi': bool(document.Vergi_levhasi and document.Vergi_levhasi.name),
    'yetki_belgesi': bool(document.Yetki_belgesi and document.Yetki_belgesi.name),
}
    
    
    print(is_files_uploaded)


    all_files_uploaded = all(is_files_uploaded.values())


    request.session['is_files_uploaded'] = is_files_uploaded
    request.session['all_files_uploaded'] = all_files_uploaded

    is_application_sended = {
        'kep_talebi':bool(document.kep_talebi), # Vergi Levhasi ve Yetki Belgesi
        'web_sitesi_talebi':bool(document.web_sitesi_talebi), # Yetki Belgesi ve Kurulus Sozlesmesi
        'sanal_pos_talebi':bool(document.sanal_pos_talebi), # Ticaret Sicil Tasdiknamesi ve Vergi Levhasi
        'hgs_talebi':bool(document.hgs_talebi), # Sirketin Mali Bilgileri ve Ticaret Sicil Dosyasi
        'hat_talebi':bool(document.hat_talebi), # Kurulus Sozlesmesi ve Sirketin Mali Bilgileri
        'fiziksel_pos_talebi':bool(document.fiziksel_pos_talebi), # Oda Kayit Belgesi ve Kurulus Sozlesmesi 
        'bulut_hizmeti_talebi':bool(document.bulut_hizmeti_talebi), # Imza Sirkuleri ve Oda Kayit Belgesi
        'banka_hesabi_acilisi_talebi':bool(document.banka_hesabi_acilisi_talebi), # Faaliyet Belgesi ve Imza Sirkuleri
        'adres_degisikligi':bool(document.adres_degisikligi), # Calisma Ruhsati ve Faaliyet Belgesi
        }
    
    request.session['is_application_sended'] = is_application_sended


    


  


    return render(request, 'upload/documents.html' , {'is_files_uploaded': is_files_uploaded , 'all_files_uploaded': all_files_uploaded , 'is_application_sended':is_application_sended})

#--------------------------------------------------------------------------------------------------------
@login_required(login_url='/users/documents')
def calisma_ruhsati(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  # Hazli hazirda dosya yoksa yeni dosya olusturur

    # Varolan Dosyayi silme 
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Calisma_ruhsati_izinler.delete(save=True)
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    # Dosya Yukleme
    if request.method == 'POST' and request.POST.get('action') == 'submit' :
        form = forms.Calisma_ruhsati_izinler(request.POST, request.FILES, instance=document)
        print(request.FILES)  # Check if the file is being sent
        print(form.errors)



        if form.is_valid():  
            form.save()
            file = document.Calisma_ruhsati_izinler.name
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")

    


    else:
        form = forms.Calisma_ruhsati_izinler(instance=document)


    if document.Calisma_ruhsati_izinler:
        is_uploaded = True

    if document.Calisma_ruhsati_izinler:
        pdf_path = document.Calisma_ruhsati_izinler
        print(pdf_path)
    else:
        pdf_path = None

    return render(request, 'upload/calisma_ruhsati.html', context= {'form':form ,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path })



#--------------------------------------------------------------------------------------------------------
@login_required(login_url='/users/documents')
def faaliyet_belgesi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Faaliyet_belgesi.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Faaliyet_belgesi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Faaliyet_belgesi.name
            
            
        else:
             messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Faaliyet_belgesi(instance=document)
    
    if document.Faaliyet_belgesi:
        is_uploaded = True

    if document.Faaliyet_belgesi:
        pdf_path = document.Faaliyet_belgesi
        print(pdf_path)
    else:
        pdf_path = None

    return render(request, 'upload/faaliyet_belgesi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})
#--------------------------------------------------------------------------------------------------------


@login_required(login_url='/users/documents')
def imza_sirkuleri(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Imza_sirkuleri.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Imza_sirkuleri(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Imza_sirkuleri.name
            
            
        else:
             messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Imza_sirkuleri(instance=document)

    if document.Imza_sirkuleri:
        is_uploaded = True

    if document.Imza_sirkuleri:
        pdf_path = document.Imza_sirkuleri
        print(pdf_path)
    else:
        pdf_path = None

    return render(request, 'upload/imza_sirkuleri.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})

#--------------------------------------------------------------------------------------------------------
@login_required(login_url='/users/documents')
def oda_kayit_belgesi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Oda_kayit_belgesi.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Oda_kayit_belgesi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Oda_kayit_belgesi.name
            
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Oda_kayit_belgesi(instance=document)

    if document.Oda_kayit_belgesi:
        is_uploaded = True

    if document.Oda_kayit_belgesi:
        pdf_path = document.Oda_kayit_belgesi
        print(pdf_path)
    else:
        pdf_path = None
    return render(request, 'upload/oda_kayit_belgesi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})
#--------------------------------------------------------------------------------------------------------

@login_required(login_url='/users/documents')
def kurulus_sozlesmesi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Kurulus_sozlemesi.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Kurulus_sozlemesi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Kurulus_sozlemesi.name
            
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Kurulus_sozlemesi(instance=document)

    if document.Kurulus_sozlemesi:
        is_uploaded = True

    if document.Kurulus_sozlemesi:
        pdf_path = document.Kurulus_sozlemesi
        print(pdf_path)
    else:
        pdf_path = None

    return render(request, 'upload/kurulus_sozlesmesi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})

#--------------------------------------------------------------------------------------------------------
@login_required(login_url='/users/documents')
def sirketin_mali_bilgileri(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Sirketin_mali_bilgileri.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Sirketin_mali_bilgileri(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Sirketin_mali_bilgileri.name
            
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Sirketin_mali_bilgileri(instance=document)

    if document.Sirketin_mali_bilgileri:
        is_uploaded = True

    if document.Sirketin_mali_bilgileri:
        pdf_path = document.Sirketin_mali_bilgileri
        print(pdf_path)
    else:
        pdf_path = None


    return render(request, 'upload/sirketin_mali_bilgileri.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})
#--------------------------------------------------------------------------------------------------------

@login_required(login_url='/users/documents')
def ticaret_sicil_odasi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user) 

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Ticaret_sicil_gazetesi.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

   
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Ticaret_sicil_gazetesi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Ticaret_sicil_gazetesi.name
            messages.success(request, "Çalışma Ruhsatı ve İzinler successfully uploaded.")
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Ticaret_sicil_gazetesi(instance=document)

    if document.Ticaret_sicil_gazetesi:
        is_uploaded = True

    if document.Ticaret_sicil_gazetesi:
        pdf_path = document.Ticaret_sicil_gazetesi
        print(pdf_path)
    else:
        pdf_path = None

    return render(request, 'upload/ticaret_sicil_odasi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})
#--------------------------------------------------------------------------------------------------------

@login_required(login_url='/users/documents')
def ticaret_sicil_tasdiknamesi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Ticaret_sicil_tasdiknamesi.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Ticaret_sicil_tasdiknamesi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Ticaret_sicil_tasdiknamesi.name
            
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Ticaret_sicil_tasdiknamesi(instance=document)

    if document.Ticaret_sicil_tasdiknamesi:
        is_uploaded = True

    if document.Ticaret_sicil_tasdiknamesi:
        pdf_path = document.Ticaret_sicil_tasdiknamesi
        print(pdf_path)
    else:
        pdf_path = None

    return render(request, 'upload/ticaret_sicil_tasdiknamesi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})
#--------------------------------------------------------------------------------------------------------


@login_required(login_url='/users/documents')
def vergi_levhasi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user)  

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Vergi_levhasi.delete()
        document.save()
        messages.success(request, "Dosya Basari ile olusturuldu")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Vergi_levhasi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Vergi_levhasi.name
            
            
        else:
            messages.error(request, "Yukleme esnasinda bir problem olustu")
    else:
        form = forms.Vergi_levhasi(instance=document)

    if document.Vergi_levhasi:
        is_uploaded = True

    if document.Vergi_levhasi:
        pdf_path = document.Vergi_levhasi
        print(pdf_path)
    else:
        pdf_path = None


    return render(request, 'upload/vergi_levhasi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})

#--------------------------------------------------------------------------------------------------------
@login_required(login_url='/users/documents')
def yetki_belgesi(request):
    file = None
    is_uploaded = False
    try:
        document = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        document = Documents(email=request.user) 

    
    if request.method == 'POST' and request.POST.get('action') == 'clear':
        document.Yetki_belgesi.delete()
        document.save()
        messages.success(request, "File successfully cleared.")
        print(request.user)
        

    
    if request.method == 'POST' and request.POST.get('action') == 'submit':
        form = forms.Yetki_belgesi(request.POST, request.FILES, instance=document)
        print(request.FILES)  
        print(form.errors)

        if form.is_valid():
            form.save()
            file = document.Yetki_belgesi.name
            messages.success(request, "Çalışma Ruhsatı ve İzinler successfully uploaded.")
            
        else:
            messages.error(request, "There was an issue with the upload. Please try again.")
    else:
        form = forms.Yetki_belgesi(instance=document)

    
    if document.Yetki_belgesi:
        is_uploaded = True

    if document.Yetki_belgesi:
        pdf_path = document.Yetki_belgesi
        print(pdf_path)
    else:
        pdf_path = None


    return render(request, 'upload/yetki_belgesi.html', context= {'form':form,'file':file,'is_uploaded':is_uploaded,'pdf_path':pdf_path})
#--------------------------------------------------------------------------------------------------------


@login_required(login_url='/users/documents')
def talepler(request):
    document = Documents.objects.get(email=request.user)

    is_files_uploaded = {
    'calisma_ruhsati': bool(document.Calisma_ruhsati_izinler and document.Calisma_ruhsati_izinler.name), 
    'faaliyet_belgesi': bool(document.Faaliyet_belgesi and document.Faaliyet_belgesi.name),
    'imza_sirkuleri': bool(document.Imza_sirkuleri and document.Imza_sirkuleri.name),
    'oda_kayit_belgesi': bool(document.Oda_kayit_belgesi and document.Oda_kayit_belgesi.name),
    'kurulus_sozlesmesi': bool(document.Kurulus_sozlemesi and document.Kurulus_sozlemesi.name),
    'sirketin_mali_bilgileri': bool(document.Sirketin_mali_bilgileri and document.Sirketin_mali_bilgileri.name),
    'ticaret_sicil_odasi': bool(document.Ticaret_sicil_gazetesi and document.Ticaret_sicil_gazetesi.name),
    'ticaret_sicil_tasdiknamesi': bool(document.Ticaret_sicil_tasdiknamesi and document.Ticaret_sicil_tasdiknamesi.name),
    'vergi_levhasi': bool(document.Vergi_levhasi and document.Vergi_levhasi.name),
    'yetki_belgesi': bool(document.Yetki_belgesi and document.Yetki_belgesi.name),
}
    is_application_sended = {
        'kep_talebi':bool(document.kep_talebi),
        'web_sitesi_talebi':bool(document.web_sitesi_talebi), 
        'sanal_pos_talebi':bool(document.sanal_pos_talebi), 
        'hgs_talebi':bool(document.hgs_talebi), 
        'hat_talebi':bool(document.hat_talebi), 
        'fiziksel_pos_talebi':bool(document.fiziksel_pos_talebi), 
        'bulut_hizmeti_talebi':bool(document.bulut_hizmeti_talebi), 
        'banka_hesabi_acilisi_talebi':bool(document.banka_hesabi_acilisi_talebi), 
        'adres_degisikligi':bool(document.adres_degisikligi), 

    }
    
    all_files_uploaded = all(is_files_uploaded.values())


    request.session['is_application_sended'] = is_application_sended
    request.session['is_files_uploaded'] = is_files_uploaded
    request.session['all_files_uploaded'] = all_files_uploaded


    return render(request , 'upload/talepler.html'  , {'is_files_uploaded': is_files_uploaded , 'all_files_uploaded': all_files_uploaded, 'is_application_sended':is_application_sended})



def all_files_uploaded(request):
    
    return render(request, 'upload/all_files_uploaded.html')



#----------------------- TALEPLERIN VIEW KISMI --------------------------------#

#----------------------------------KEP TALEBI------------------------------------------------#

def kep_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['vergi_levhasi'] and is_files_uploaded['yetki_belgesi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
            if is_files_uploaded['vergi_levhasi'] and is_files_uploaded['yetki_belgesi']:
                talep.kep_talebi = True
                talep.save()
                return redirect('upload:talepler')
         

            
    print(disable_button)


    print(is_files_uploaded)
    
    
    return render(request, 'upload/kep_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})

#----------------------------------WEB SITESI TALEBI------------------------------------------------#
def web_sitesi_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['kurulus_sozlesmesi'] and is_files_uploaded['yetki_belgesi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['kurulus_sozlesmesi'] and is_files_uploaded['yetki_belgesi']:
            talep.web_sitesi_talebi = True
            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/web_sitesi_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------------------SANAL POS TALEBI------------------------------------------------#
def sanal_pos_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['ticaret_sicil_tasdiknamesi'] and is_files_uploaded['vergi_levhasi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['ticaret_sicil_tasdiknamesi'] and is_files_uploaded['vergi_levhasi']:
            talep.sanal_pos_talebi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/sanal_pos_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------------------HAT TALEBI------------------------------------------------#
def hat_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['kurulus_sozlesmesi'] and is_files_uploaded['sirketin_mali_bilgileri'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['kurulus_sozlesmesi'] and is_files_uploaded['sirketin_mali_bilgileri']:
            talep.hat_talebi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/hat_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------------------FIZIKSEL POS TALEBI------------------------------------------------#
def fiziksel_pos_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['oda_kayit_belgesi'] and is_files_uploaded['kurulus_sozlesmesi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['oda_kayit_belgesi'] and is_files_uploaded['kurulus_sozlesmesi']:
            talep.fiziksel_pos_talebi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/fiziksel_pos_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------------------BULUT HIZMETI TALEBI------------------------------------------------#
def bulut_hizmeti_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['imza_sirkuleri'] and is_files_uploaded['oda_kayit_belgesi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['imza_sirkuleri'] and is_files_uploaded['oda_kayit_belgesi']:
            talep.bulut_hizmeti_talebi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/bulut_hizmeti_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------------------BANKA HESABI ACILISI TALEBI------------------------------------------------#

def banka_hesabi_acilisi_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['faaliyet_belgesi'] and is_files_uploaded['imza_sirkuleri'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['faaliyet_belgesi'] and is_files_uploaded['imza_sirkuleri']:
            talep.banka_hesabi_acilisi_talebi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    
    return render(request, 'upload/banka_hesabi_acilisi_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------------------ADRESS DEGISIKLIGI TALEBI------------------------------------------------#
def adres_degisikligi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['calisma_ruhsati'] and is_files_uploaded['faaliyet_belgesi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['calisma_ruhsati'] and is_files_uploaded['faaliyet_belgesi']:
            talep.adres_degisikligi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/adres_degisikligi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})

#----------------------------------HGS TALEBI------------------------------------------------#
def hgs_talebi(request):

    is_files_uploaded = request.session.get('is_files_uploaded', {})
    all_files_uploaded = request.session.get('all_files_uploaded', False)

    disable_button = (is_files_uploaded['sirketin_mali_bilgileri'] and is_files_uploaded['ticaret_sicil_odasi'])

    try:
        talep = Documents.objects.get(email=request.user)
    except Documents.DoesNotExist:
        talep = Documents(email=request.user)

    if request.method == 'POST' :
        if request.POST.get('action') == 'create_request':
         if is_files_uploaded['sirketin_mali_bilgileri'] and is_files_uploaded['ticaret_sicil_odasi']:
            talep.hgs_talebi = True

            talep.save()

    print(disable_button)


    print(is_files_uploaded)
    
    return render(request, 'upload/hgs_talebi.html', {'is_files_uploaded': is_files_uploaded, 'all_files_uploaded': all_files_uploaded ,'disable_button': disable_button})
#----------------------- TALEPLERIN VIEW KISMI --------------------------------#



#VER 0.2