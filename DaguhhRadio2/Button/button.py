
# test_bouton=============================================================
# Import des modules
from RPi import GPIO
import time

# Initialisation de la numerotation et des E/S
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.IN)

# Si on detecte un appui sur le bouton, on allume la LED 
# et on attend que le bouton soit relache
while True:
    state = GPIO.input(23)
    print(state)
    time.sleep(1)
#    if not state