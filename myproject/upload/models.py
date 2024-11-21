import os
from django.db import models
from .file_validation import validate_file_extension
from django.contrib.auth.models import User


def upload_to_company_folder(instance, filename):
    
    return os.path.join(f"documents/{instance.email}", filename)

class Documents(models.Model):
    Sirket_tipi = models.CharField(max_length=10)
    Kurulus_sozlemesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Vergi_levhasi =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Ticaret_sicil_gazetesi =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Imza_sirkuleri =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Oda_kayit_belgesi =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Yetki_belgesi =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Faaliyet_belgesi =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Calisma_ruhsati_izinler =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    Sirketin_mali_bilgileri =  models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension],blank=True)
    Ticaret_sicil_tasdiknamesi = models.FileField(upload_to=upload_to_company_folder, validators=[validate_file_extension], blank=True)
    tarih = models.DateTimeField(auto_now_add=True)

    email = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    

    kep_talebi = models.BooleanField(default=False)
    web_sitesi_talebi = models.BooleanField(default=False)
    sanal_pos_talebi = models.BooleanField(default=False)
    hgs_talebi = models.BooleanField(default=False)
    hat_talebi = models.BooleanField(default=False)
    fiziksel_pos_talebi = models.BooleanField(default=False)
    bulut_hizmeti_talebi = models.BooleanField(default=False)
    banka_hesabi_acilisi_talebi = models.BooleanField(default=False)
    adres_degisikligi = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
       
        file_fields = [
            self.Kurulus_sozlemesi,
            self.Vergi_levhasi,
            self.Ticaret_sicil_gazetesi,
            self.Imza_sirkuleri,
            self.Oda_kayit_belgesi,
            self.Yetki_belgesi,
            self.Faaliyet_belgesi,
            self.Calisma_ruhsati_izinler,
            self.Sirketin_mali_bilgileri,
            self.Ticaret_sicil_tasdiknamesi,
        ]

        for file_field in file_fields:
            if file_field and os.path.isfile(file_field.path):
                os.remove(file_field.path)  

       
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.email.email
