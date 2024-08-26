from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from . import models

@admin.register(models.MasterPetugas)
class PersonAdmin(ImportExportModelAdmin):
    pass

admin.site.register(models.AlokasiPetugas)
admin.site.register(models.RoleMitra)
