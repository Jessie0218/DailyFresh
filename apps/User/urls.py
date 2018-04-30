from django.conf.urls import url
from apps.User.views import LoginView, RegisterView

urlpatterns = [
    url(r'^login.html$', LoginView.as_view(), name='login'),
    url(r'^register.html$', RegisterView.as_view(), name='register')
]