import picamera
import io
import time


"""
This was really slow to process frame at a time. This comes from the
camera.py documentation, how to capture JPEG frames as fast as possible
into an in-memory stream.
"""
with picamera.PiCamera() as camera:
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, format='jpeg'):
        # Truncate the stream to the current position (in case
        # prior iterations output a longer image)
        stream.truncate()
        stream.seek(0)
        print(foo)
