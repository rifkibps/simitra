from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeClassView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'title' : 'Home Page'
        }
        return render(request, 'home/index.html', context)

