from django.db import models


# Create your models here.
class SurveyModel(models.Model):
   
   status = (
       ('0', 'Aktif'),
       ('1', 'Non Aktif'),
       ('2', 'Selesai')
   )
   
   nama = models.CharField(max_length=128, null=False, blank=False, verbose_name='Nama Survei' )
   deskripsi = models.TextField(null=False, blank=False, verbose_name='Deskripsi Survei')
   tgl_mulai = models.DateField( null=False, blank=False, verbose_name='Tanggal Mulai')
   tgl_selesai = models.DateField( null=False, blank=False, verbose_name='Tanggal Berakhir')
   status = models.CharField(max_length=1, choices=status, default=0, null=False, blank=False, verbose_name='Status Survei')
   

   def __str__(self):
      return f"{self.nama} [{self.tgl_mulai} s.d. {self.tgl_selesai}]"