from gpiozero import LED
from gpiozero import Button
from picamera import PiCamera
import json
import cv2
import numpy as np
from time import sleep
import os
import requests

# Set up the LEDs
led_red = LED(17)
led_green = LED(18)
led_blue = LED(27)
camera = PiCamera()
button = Button(2)

def make_request(path):
  img = cv2.imread(path)
  imgResize = np.reshape(img, 151200)
  imgJoin = '{"rgb_array": [' + ','.join(str(e) for e in imgResize) +  '] , "height": 168, "width": 300 }'
  jsonParaRequest = json.loads(imgJoin)
  hello = requests.post('https://backfreeze-ocr.herokuapp.com/img_to_str/', json = jsonParaRequest)
  print(hello)
  os.remove(path)


while True:
  led_blue.on()

  button.wait_for_press()
  led_blue.off()
  led_green.on()
  sleep(5)
  camera.capture('/home/pi/Desktop/image.jpg')
  make_request('/home/pi/Desktop/image.jpg')
  led_green.off()
  




