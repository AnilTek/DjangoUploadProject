from django import forms
from . import models


 #fields = ['Kurulus_sozlemesi','Vergi_levhasi','Ticaret_sicil_gazetesi','Imza_sirkuleri','Oda_kayit_belgesi','Yetki_belgesi','Faaliyet_belgesi','Calisma_ruhsati_izinler','Sirketin_mali_bilgileri','Ticaret_sicil_tasdiknamesi']

class Calisma_ruhsati_izinler(forms.ModelForm):
   class Meta:
        model = models.Documents
      
        fields = ['Calisma_ruhsati_izinler']
class Faaliyet_belgesi(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Faaliyet_belgesi']
class Imza_sirkuleri(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Imza_sirkuleri']
class Oda_kayit_belgesi(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Oda_kayit_belgesi']
class Kurulus_sozlemesi(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Kurulus_sozlemesi']
class Sirketin_mali_bilgileri(forms.ModelForm):
   class Meta:
        model = models.Documents
       
        fields = ['Sirketin_mali_bilgileri']
class Ticaret_sicil_gazetesi(forms.ModelForm):
   class Meta:
        model = models.Documents
       
        fields = ['Ticaret_sicil_gazetesi']
class Ticaret_sicil_tasdiknamesi(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Ticaret_sicil_tasdiknamesi']
class Vergi_levhasi(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Vergi_levhasi']
class Yetki_belgesi(forms.ModelForm):
   class Meta:
        model = models.Documents
        
        fields = ['Yetki_belgesi']