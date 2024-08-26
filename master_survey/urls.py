from django.urls import path
from . import views

app_name = 'master_survei'

urlpatterns = [
    path('master-survei', views.MasterSurveiClassView.as_view(), name='index'),
    path('master-survei/json-response', views.SurveyJsonResponseClassView.as_view(), name='datatable-json'),
    path('master-survei/delete', views.MasterSurveyDeleteView.as_view(), name='delete-survey'),
    path('master-survei/detail', views.MasterSurveyDetailView.as_view(), name='detail-survey'),
    path('master-survei/update', views.MasterSurveyUpdateView.as_view(), name='update-survey'),
    path('master-survei/export', views.MasterSurveyExportView.as_view(), name='export-survey'),
    path('master-survei/upload', views.MasterSurveyUploadClassView.as_view(), name='upload-survey'),
    path('master-survei/template/<int:rows>', views.MasterSurveyTemplateClassView.as_view(), name='template-survey'),

]