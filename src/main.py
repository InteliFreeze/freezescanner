from gpiozero import LED
from gpiozero import Button
from picamera import PiCamera
import json
import base64
import cv2
import numpy as np
from time import sleep
import os
import requests

# Set up the LEDs
led_red = LED(17)
led_green = LED(18)
rgb_green = LED(22)
rgb_blue = LED(23)
camera = PiCamera()
button = Button(2)

def make_request_ocr(path):
  img = cv2.imread(path)
  _, im_arr = cv2.imencode(".jpg", img)
  im_bytes = im_arr.tobytes()
  im_b64 = base64.b64encode(im_bytes)
  
  hello = requests.post("https://backfreeze.herokuapp.com/api/receitas/ocr?base64=" + str(im_b64)[2:])

  os.remove(path)
  return hello.text


def make_request_barcode(path):
  img = cv2.imread(path)
  _, im_arr = cv2.imencode(".jpg", img)
  im_bytes = im_arr.tobytes()
  im_b64 = base64.b64encode(im_bytes)
  
  json_para_request = {"base64_img": str(im_b64)[2:]}
  
  hello = requests.post('https://backfreeze-ocr.herokuapp.com/barcode/', json = json_para_request)
  os.remove(path)
  return hello.text
  
# "https://backfreeze.herokuapp.com/api/users/usertoken?item=laranja&validade=2022-04-20&codigo=434325643"

isbarcode = False
url = "https://backfreeze.herokuapp.com/api/users/usertoken?item=PREENCHER&validade=VALIDADE&codigo=BARCODE"

while True:
    if button.is_pressed and (not isbarcode):
        rgb_blue.on()
        led_red.off()
        camera.start_preview()
        sleep(3)
        camera.stop_preview()
        camera.capture('/home/intelifreeze/Desktop/image.jpg')
        validade = make_request_ocr('/home/intelifreeze/Desktop/image.jpg')
        url.replace("VALIDADE", validade)
        rgb_blue.off()
        isbarcode = True
    elif button.is_pressed and isbarcode:
        rgb_blue.on()
        led_red.off()
        camera.start_preview()
        sleep(3)
        camera.stop_preview()
        camera.capture('/home/intelifreeze/Desktop/image.jpg')
        codigo = make_request_barcode('/home/intelifreeze/Desktop/image.jpg')
        url.replace("BARCODE", codigo)
        requests.post(url)
        sleep(1)
        url = "https://backfreeze.herokuapp.com/api/users/usertoken?item=PREENCHER&validade=VALIDADE&codigo=BARCODE"
        rgb_blue.off()
        isbarcode = False
    else:
        led_red.on()
        sleep(0.1)
  






