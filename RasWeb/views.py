from django.shortcuts import render
from django.http import HttpResponse, Http404
import time
import RPi.GPIO as GPIO 

# Create your views here.
def index(request):
    return render(request, "RasWeb/index.html")

LED_PIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

def status(request, stt):   
    if stt == 'on':
        GPIO.output(LED_PIN, GPIO.HIGH)
        return HttpResponse()     
    elif stt == 'off':
        GPIO.output(LED_PIN, GPIO.LOW)
        return HttpResponse()
    elif stt == 'blink':
        for i in range(10):
            GPIO.output(LED_PIN, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(LED_PIN, GPIO.LOW)
            time.sleep(0.5)
        return HttpResponse()
    else:
        return Http404('No such status')