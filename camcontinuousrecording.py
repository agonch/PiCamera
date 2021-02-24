import io
import picamera
import sys
import time
from PIL import Image

stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.vflip = True
    camera.framerate = 24
    camera.resolution = (1280, 720)
    camera.start_preview()
    time.sleep(2)

    # camera.start_recording("my_movie.h264")
    # time.sleep(5)
    # camera.stop_recording()

    # camera.start_recording(stream, format='h264', quality=23)
    # # Note bitrate can be controlled, but depends on profile and
    # # h264 level https://en.wikipedia.org/wiki/Advanced_Video_Coding#Levels
    # camera.wait_recording(5)
    # camera.stop_recording()

    camera.start_recording(stream, format='h264', quality=23)
    print("Started recording")
    try:
        while sys.getsizeof(stream) < 2000000:
            print("sizeof", sys.getsizeof(stream))
            time.sleep(1)
        camera.stop_recording()
        with io.open('motion.h264', 'wb') as output:
            stream.seek(0)
            output.write(stream.read())
    finally:
        camera.stop_recording()
        stream.flush()
