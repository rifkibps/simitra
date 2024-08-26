from django.shortcuts import render
from django.views import View

from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.conf import settings

from . import models
from . import forms

# Superuser account
# username: rifki.gusti
# password: hbz934115

class LoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    extra_context = {
        'title' : 'Login Page'
    }

class LogoutView(LogoutView):
    next_page = settings.LOGIN_URL
    extra_context = {
        'page_header' : 'Halaman Login'
    }


class UserThemeSetClassView(LoginRequiredMixin, View):

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:

            data = request.POST

            model = models.Profile.objects.get(user = request.user.id)

            if data.get('theme_dark'):
                model.theme = '1' if model.theme == '0' else '0'

            if data.get('condense_menu'):
                model.theme_condense = '1' if model.theme_condense == '0' else '0'
           
            model.save()   
            
            # send to client side.
            return JsonResponse({"status": 'success', 'message': 'Data berhasil diubah'}, status=200)
        
        return JsonResponse({"error": ""}, status=400)
    

class UserAccountClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'User Account',
            'form' : forms.ProfileUpdateForm(),
            'users_groups' : ', '.join(request.user.groups.values_list('name',flat = True))
        }
    
        return render(request, 'authentication/account.html', context)
    

    def post(self, request):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            form = forms.ProfileUpdateForm(request.FILES)
            if form.is_valid():
                model = models.Profile.objects.get(user = self.request.user.id)
                model.image = form.data.get('image')
                model.save()

                return JsonResponse({"status": "success", 'message':'Data berhasil diupdate'}, status=200)

        return JsonResponse({"status": "failed", "message" : 'Request needed'}, status=400)