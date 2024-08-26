from import_export import resources, widgets

from import_export.fields import Field
from . import models

class MasterSurveiResource(resources.ModelResource):

    nama = Field(attribute="nama", column_name="Nama Survei")
    deskripsi = Field(attribute="deskripsi", column_name="Deskripsi Survei")
    tgl_mulai = Field(attribute="tgl_mulai", column_name="Tanggal Mulai Survei", widget=widgets.DateWidget("%d/%m/%Y"))
    tgl_selesai = Field(attribute="tgl_selesai", column_name="Tanggal Selesai Survei", widget=widgets.DateWidget("%d/%m/%Y"))
    status = Field(attribute="get_status_display", column_name="Status Survei")

    class Meta:
        model = models.SurveyModel
        fields = (
            'nama',
            'deskripsi',
            'tgl_mulai',
            'tgl_selesai',
            'status',
        )
        