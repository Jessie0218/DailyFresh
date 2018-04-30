from django.shortcuts import render
from django.views.generic import View
from apps.User.models import User
from django.core.mail import send_mail
import re
from DailyFresh import settings


# Create your views here.
class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')