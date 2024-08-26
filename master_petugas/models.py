from django.db import models
from master_survey.models import SurveyModel
from .validators import int_validators

# Create your models here.
class MasterPetugas(models.Model):

    status_choices = (
       ('0', 'Aktif'), ('1', 'Non Aktif'), ('2', 'Organik'), ('3', 'Blacklist')
    )

    pendidikan = (
       ('0', 'SD/MI Sederajat'), 
       ('1', 'SMP/SLTP Sederajat'),
       ('2', 'SMA/SLTA Sederajat'),
       ('3', 'DI-DIII'),
       ('4', 'DV/S1'),
       ('5', 'S2'),
       ('6', 'S3')
    )
    

    agama = (
       ('0', 'Islam'), 
       ('1', 'Kristen'),
       ('2', 'Hindu'),
       ('3', 'Budha'),
    )

    kode_petugas = models.CharField(max_length=16, null=False, blank=False, unique=True, verbose_name='Kode Petugas/ID Sobat')
    nama_petugas = models.CharField(max_length=64, null=False, blank=False,  verbose_name='Nama Petugas')
    nik = models.CharField(max_length=16, null=False, blank=False, validators=[int_validators], unique=True, verbose_name='NIK')
    npwp = models.CharField(max_length=15, null=False, blank=False, validators=[int_validators], unique=True, verbose_name='NPWP')
    tgl_lahir = models.DateField(auto_now=False, auto_now_add=False, null=False, blank=False, verbose_name='Tanggal Lahir')
    pendidikan = models.CharField(max_length=1, choices=pendidikan, null=False, blank=False, verbose_name='Pendidikan Terakhir')
    pekerjaan = models.CharField(max_length=128, null=False, blank=False, verbose_name='Pekerjaan')
    agama = models.CharField(max_length=1, choices=agama, null=False, blank=False, verbose_name='Agama')
    email = models.EmailField(max_length=128, null=False, blank=False,unique=True, verbose_name='Email')
    no_telp = models.CharField(max_length=13, null=False, blank=False, validators=[int_validators], verbose_name='No. Telp')
    alamat = models.CharField(max_length=256, null=False, blank=False, verbose_name='Alamat Domisili')
    
    status = models.CharField(max_length=1, choices=status_choices, blank=False, verbose_name='Status Mitra')
    
    def __str__(self):
        return f"{self.nama_petugas} [{self.kode_petugas}]"

class RoleMitra(models.Model):
   jabatan = models.CharField(max_length=128, null=False, blank=False, verbose_name='Jabatan/Peran')
   def __str__(self):
         return f"{self.jabatan}"
   

class AlokasiPetugas(models.Model):

   petugas = models.ForeignKey(MasterPetugas, on_delete=models.RESTRICT, related_name='master_alokasi_petugas', verbose_name='Kode Petugas')
   survey = models.ForeignKey(SurveyModel, on_delete=models.RESTRICT, related_name='master_alokasi_survey', verbose_name='Survei/Sensus')
   role = models.ForeignKey(RoleMitra, on_delete=models.RESTRICT, related_name='master_alokasi_role', verbose_name='Jabatan Petugas')

   def __str__(self):
      return f"{self.petugas.nama_petugas} [{self.petugas.kode_petugas} - {self.survey.nama}_{self.role.jabatan}]"
   
