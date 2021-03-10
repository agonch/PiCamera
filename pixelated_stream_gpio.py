# coding=utf-8

import RPi.GPIO as GPIO
import datetime
import io
import picamera
from picamera.array import PiRGBArray
import time
from PIL import Image
import sys
import cv2
import numpy as np

"""
Streamed continously into an RGB Array:
 https://picamera.readthedocs.io/en/release-1.10/api_array.html#pirgbarray
 https://picamera.readthedocs.io/en/release-1.10/api_camera.html#picamera.camera.PiCamera.capture_continuous    
"""

np.set_printoptions(threshold=sys.maxsize)
RESOLUTION = (640, 480)
PIXELATED_RESOLUTION = (64, 64)
SHOULD_FLIP_RGB = False

def flipRGB(rgb_array):
    return rgb_array[:, :, ::-1]


"""
Grab the input size of the PiRGBArray, and resize the input to
"pixelated" size. Return output image.
"""
def pixelateFrame(rgb_array):
    if SHOULD_FLIP_RGB:
        rgb_array = flipRGB(rgb_array)
    height, width = rgb_array.shape[:2]
    temp = cv2.resize(rgb_array, PIXELATED_RESOLUTION, interpolation=cv2.INTER_LINEAR)
    output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)
    return output


def prepCamera(camera):
    camera.vflip = True
    camera.resolution = RESOLUTION
    camera.framerate = 30
    # Now fix the values
    # camera.shutter_speed = camera.exposure_speed
    # camera.exposure_mode = 'off'
    # g = camera.awb_gains
    # camera.awb_mode = 'off'
    # camera.awb_gains = g
    return camera


def gpio_callback(channel):
    global SHOULD_FLIP_RGB
    SHOULD_FLIP_RGB = GPIO.input(channel) == GPIO.HIGH
    if GPIO.input(channel) == GPIO.HIGH:
        print('\n▼  at ' + str(datetime.datetime.now()))
    else:
        print('\n ▲ at ' + str(datetime.datetime.now()))


def launch_camera():
    with picamera.PiCamera() as camera:
        stream = io.BytesIO()
        prepCamera(camera)
        time.sleep(1)
        with PiRGBArray(camera, size=RESOLUTION) as rawPiStream:
            for frame in camera.capture_continuous(rawPiStream, format="bgr", use_video_port=True):
                cv2.imshow('Input', frame.array)
                cv2.imshow('Output', pixelateFrame(frame.array))
                rawPiStream.truncate(0)
                # Return if the `q` key was pressed
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(6, GPIO.BOTH, callback=gpio_callback)
    launch_camera()
finally:
    GPIO.cleanup()
    print("Goodbye!")