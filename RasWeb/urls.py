from django.urls import path
from . import views

app_name = 'light_control'
urlpatterns = [
    path('', views.index, name='index'),
    path('on', views.turn_on, name='turn_on'),
    path('off', views.turn_off, name='turn_off'),
    path('blink', views.blink, name='blink')
]