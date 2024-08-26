from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.MainDashboardClassView.as_view(), name='index'),
    path('dashboard/ranking', views.DashboardRankClassView.as_view(), name='rank')
]