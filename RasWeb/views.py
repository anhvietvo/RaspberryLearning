from django.shortcuts import render
import time
import RPi.GPIO as GPIO 

# Create your views here.
def index(request):
    return render(request, "RasWeb/index.html")

LED_PIN = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN, GPIO.OUT)

def turn_on(request):
    GPIO.output(LED_PIN, GPIO.HIGH)
    return render(request, "RasWeb/index.html", {
        "status": "on"
    })

def turn_off(request):
    GPIO.output(LED_PIN, GPIO.LOW)
    return render(request, "RasWeb/index.html", {
        "status": "off"
    })

def blink(request):
    for i in range(10):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(1)
    return render(request, "RasWeb/index.html")
 