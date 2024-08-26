from import_export import resources, widgets
from import_export.fields import Field
from .models import MasterNilaiPetugas, KegiatanPenilaianModel, IndikatorKegiatanPenilaian

class MasterKegiatanResource(resources.ModelResource):

    nama_kegiatan = Field(attribute="nama_kegiatan", column_name="Nama Kegiatan")
    survey = Field(attribute="survey", column_name="Nama Survei")
    tgl_penilaian = Field(attribute="tgl_penilaian", column_name="Tanggal Penilaian", widget=widgets.DateWidget(format=None))
    status = Field(attribute="get_status_display", column_name="Status Kegiatan")

    class Meta:
        model = KegiatanPenilaianModel
        fields = (
            'nama_kegiatan',
            'survey',
            'tgl_penilaian',
            'status'
        )

class MasterNilaiResource(resources.ModelResource):
    
    petugas__petugas__kode_petugas = Field(attribute="petugas__petugas__kode_petugas", column_name="ID Mitra")
    petugas__petugas__nama_petugas = Field(attribute="petugas__petugas__nama_petugas", column_name="Nama Mitra")
    penilaian__kegiatan_penilaian__survey__nama = Field(attribute="penilaian__kegiatan_penilaian__survey__nama", column_name="Nama Kegiatan Survei/Sensus")
    petugas__role__jabatan = Field(attribute="petugas__role__jabatan", column_name="Jabatan")
    penilaian__kegiatan_penilaian__nama_kegiatan =  Field(attribute="penilaian__kegiatan_penilaian__nama_kegiatan", column_name="Kegiatan Penilaian")
    penilaian__indikator_penilaian__nama_indikator = Field(attribute="penilaian__indikator_penilaian__nama_indikator", column_name="Indikator Penilaian")
    nilai = Field(attribute="nilai", column_name="Nilai Mitra")
    catatan = Field(attribute="catatan", column_name="Catatan Personal")
    
    class Meta:
        model = MasterNilaiPetugas
        fields = (
            'petugas__petugas__kode_petugas',
            'petugas__petugas__nama_petugas',
            'penilaian__kegiatan_penilaian__survey__nama',
            'petugas__role__jabatan',
            'penilaian__kegiatan_penilaian__nama_kegiatan',
            'penilaian__indikator_penilaian__nama_indikator',
            'nilai',
            'catatan'
        )


class IndikatorKegiatanResources(resources.ModelResource):
    
    kegiatan_penilaian__survey__nama = Field(attribute="kegiatan_penilaian__survey__nama", column_name="Nama Survei")
    kegiatan_penilaian__nama_kegiatan = Field(attribute="kegiatan_penilaian__nama_kegiatan", column_name="Nama Kegiatan Pendataan")
    indikator_penilaian__nama_indikator = Field(attribute="indikator_penilaian__nama_indikator", column_name="Indikator Kegiatan")
    
    class Meta:
        model = IndikatorKegiatanPenilaian
      
        fields = (
            'kegiatan_penilaian__survey__nama',
            'kegiatan_penilaian__nama_kegiatan',
            'indikator_penilaian__nama_indikator',
        )