import io
import picamera
import time
from PIL import Image

stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.vflip = True
    camera.resolution = (1280, 720)
    camera.start_preview()
    camera.framerate = 30
    # Wait for the automatic gain control to settle
    time.sleep(2)
    # Now fix the values
    # camera.shutter_speed = camera.exposure_speed
    # camera.exposure_mode = 'off'
    # g = camera.awb_gains
    # camera.awb_mode = 'off'
    # camera.awb_gains = g
    # Finally, take several photos with the fixed settings
    i = 0
    for s in camera.capture_continuous(stream, format='jpeg'):
        print('Captured %s' % s)
        s.seek(0)
        image = Image.open(s)
        # image.save('out%d.jpg' % i)
        s.seek(0)
        s.truncate()
        i += 1
        if i > 20:
            break
