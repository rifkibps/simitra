from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile

# Register your models here.

admin.site.register(Profile)
