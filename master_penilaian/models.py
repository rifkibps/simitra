from django.db import models
from master_survey.models import SurveyModel
from master_petugas.models import AlokasiPetugas, RoleMitra


# Create your models here.


class IndikatorPenilaian(models.Model):
   nama_indikator = models.CharField(max_length=128, null=False, blank=False, verbose_name='Indikator Penilaian' )
   deskripsi_penilaian = models.TextField(null=True, blank=True, verbose_name='Deskripsi Penilaian')

   def __str__(self):
      return f"{self.nama_indikator}"


class KegiatanPenilaianModel(models.Model):
   
    status = (
       ('0', 'Aktif'),
       ('1', 'Tidak Aktif')
    )

    nama_kegiatan = models.CharField(max_length=256, null=False, blank=False, verbose_name='Nama Kegiatan Penilaian' )
    survey = models.ForeignKey(SurveyModel, on_delete=models.RESTRICT, blank=False, null=False, related_name='penilaian_survei')
    tgl_penilaian = models.DateField( null=False, blank=False,  verbose_name='Tanggal Penilaian')
    status = models.CharField(max_length=1, choices=status, default=0, null=False, blank=False, verbose_name='Status Penilaian')
    role_permitted = models.ManyToManyField(RoleMitra)
    
    def __str__(self):
        return f"{self.nama_kegiatan} [{self.survey.nama}]"
   

class IndikatorKegiatanPenilaian(models.Model):
   kegiatan_penilaian = models.ForeignKey(KegiatanPenilaianModel, on_delete=models.RESTRICT, related_name='kegiatan_penilaian_petugas')
   indikator_penilaian = models.ForeignKey(IndikatorPenilaian, on_delete=models.RESTRICT, related_name='indikator_penilaian_petugas')
   
   def __str__(self):
      return f"{self.kegiatan_penilaian.nama_kegiatan} [{self.indikator_penilaian}]"


class MasterNilaiPetugas(models.Model):

   petugas = models.ForeignKey(AlokasiPetugas, on_delete=models.RESTRICT,  related_name='nilai_petugas')
   penilaian = models.ForeignKey(IndikatorKegiatanPenilaian, on_delete=models.RESTRICT, related_name='indikator_kegiatan_penilaian')
   nilai = models.SmallIntegerField(null=True, blank=True, verbose_name='Nilai Kegiatan Petugas')
   catatan = models.TextField(null=True, blank=True, verbose_name='Catatan Personal')

   def __str__(self):
      return f"{self.petugas.petugas.nama_petugas} [{self.penilaian.kegiatan_penilaian}]"
      
