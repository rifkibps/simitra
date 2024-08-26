from django.urls import path
from . import views

app_name = 'auth'
urlpatterns = [
    path('user-profile/', views.UserThemeSetClassView.as_view(), name='user-profile'),
    path('account/', views.UserAccountClassView.as_view(), name='user-account'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
