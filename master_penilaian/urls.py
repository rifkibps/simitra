from django.urls import path
from . import views

app_name = 'master_penilaian'

urlpatterns = [
    path('master-penilaian', views.PenilaianPetugasClassView.as_view(), name='index'),
    path('master-penilaian/json-response', views.MasterPenilaianJsonResponseClassView.as_view(), name='datatable-json'),
    path('master_penilaian/delete', views.MasterPenilaianDeleteView.as_view(), name='delete-kegiatan'),
    path('master_penilaian/detail', views.MasterPenilaianDetailView.as_view(), name='detail-kegiatan'),
    path('master_penilaian/update', views.MasterPenilaianUpdateView.as_view(), name='update-kegiatan'),
    path('master_penilaian/export', views.MasterPenilaianExportView.as_view(), name='export-kegiatan'),
    path('master_penilaian/get-penilaian-by-survey', views.PenilaianGetBySurveiClassView.as_view(), name='get-penilaian-by-survei'),
    path('master_penilaian/get-alokasi-by-survey', views.AlokasiGetBySurveiClassView.as_view(), name='get-alokasi-by-survei'),

    path('nilai-mitra', views.NilaiMitraClassView.as_view(), name='nilai-mitra'),
    path('nilai-mitra/json-response', views.NilaiMitraJsonResponseClassView.as_view(), name='nilai-mitra-json'),
    path('nilai-mitra/delete', views.NilaiMitraDeleteClassView.as_view(), name='delete-nilai-mitra'),
    path('nilai-mitra/detail', views.NilaiMitraDetailClassView.as_view(), name='detail-nilai-mitra'),
    path('nilai-mitra/update', views.NilaiMitraUpdateClassView.as_view(), name='update-nilai-mitra'),
    path('nilai-mitra/export', views.NilaiMitraExportClassView.as_view(), name='export-nilai-mitra'),
    path('nilai-mitra/template/<int:kegiatan>', views.NilaiMitraTemplateClassView.as_view(), name='template-nilai-mitra'),
    path('nilai-mitra/upload', views.NilaiMitraUploadClassView.as_view(), name='upload-nilai-mitra'),
    path('nilai-mitra/table', views.GenerateTableNilaiClassView.as_view(), name='generate-table-nilai'),
    path('nilai-mitra/get-nilai-mitra', views.GetNilaiMitraClassView.as_view(), name='get-nilai-mitra'),
    

    path('indikator-penilaian', views.IndikatorPenilaianClassView.as_view(), name='indikator-penilaian'),
    path('indikator-penilaian/json-response', views.IndiakatorPenilaianJsonResponseClassView.as_view(), name='indikator-penilaian-json'),
    path('indikator-penilaian/delete', views.IndikatorPenilaianDeleteView.as_view(), name='delete-indikator'),
    path('indikator-penilaian/detail', views.IndikatorPenilaianDetailView.as_view(), name='detail-indikator'),
    path('indikator-penilaian/update', views.IndikatorPenilaianUpdateView.as_view(), name='update-indikator'),
    
    path('indikator-kegiatan', views.IndikatorKegiatanPenilaianClassView.as_view(), name='indikator-kegiatan'),
    path('indikator-kegiatan/json-response', views.IndikatorKegiatanPenilaianJsonResponseClassView.as_view(), name='indikator-kegiatan-json'),
    path('indikator-kegiatan/delete', views.IndikatorKegiatanPenilaianDeleteView.as_view(), name='delete-indikator-kegiatan'),
    path('indikator-kegiatan/detail', views.IndikatorKegiatanPenilaianDetailView.as_view(), name='detail-indikator-kegiatan'),
    path('indikator-kegiatan/update', views.IndikatorKegiatanPenilaianUpdateView.as_view(), name='update-indikator-kegiatan'),
    path('indikator-kegiatan/export', views.IndikatorKegiatanPenilaianExportView.as_view(), name='export-indikator-kegiatan'),
]