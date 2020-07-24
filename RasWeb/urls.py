from django.urls import path
from . import views

app_name = 'light_control'
urlpatterns = [
    path('', views.index, name='index'),
]