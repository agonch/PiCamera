import io
import time
import picamera
import picamera.array
from PIL import Image
import numpy as np

# Create an in-memory stream
stream = io.BytesIO()
with picamera.PiCamera() as camera:
    camera.vflip = True
    camera.start_preview()
    # Camera warm-up time
    time.sleep(2)
    camera.capture(stream, format='jpeg')
    # camera.capture("test.jpg")
    with picamera.array.PiRGBArray(camera) as pistream:
        # CV2 has lossy decoding, this is a potential speedup
        camera.capture(pistream, format='bgr')
        # At this point the image is available as stream.array
        bgr_image = pistream.array
        rgb_image = bgr_image[:, :, ::-1] # flip the ordering 
        result = Image.fromarray(rgb_image.astype(np.uint8))
        result.save('out_pistream.bmp')


# "Rewind" the stream to the beginning so we can read its content
stream.seek(0)
image = Image.open(stream)
image.save('out.jpg')

data = np.array(image)
result = Image.fromarray(data.astype(np.uint8))
result.save('out_np.bmp')
