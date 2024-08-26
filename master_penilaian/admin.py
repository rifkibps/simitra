from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.KegiatanPenilaianModel)
admin.site.register(models.MasterNilaiPetugas)
admin.site.register(models.IndikatorPenilaian)
admin.site.register(models.IndikatorKegiatanPenilaian)



