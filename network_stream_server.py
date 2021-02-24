import socket
import time
import picamera


"""
First way:
- Run server first and then `vlc tcp/h264://127.0.0.1:8000/` on client
- Running into main input error: ES_OUT_SET_(GROUP_)PCR errors
- super jittery

An alternative way:
- server: $ raspivid -vf -n -w 640 -h 480 -t 60000 -o - | nc localhost 8000
- client: $ nc -l 8000 | vlc --demux h264 -
OR        $ nc -l localhost 8000 | vlc --demux h264 -
- There is a heavy delay

Alternatively:
- use mplayer, need cache (otherwise get `Cannot seek backward in linear streams!`)
  https://unix.stackexchange.com/questions/97046/how-to-get-mplayer-to-play-from-stdin
- $ nc -l 8000 | mplayer -fps 24 -cache 1024 -framedrop -
"""
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 30
    camera.vflip = True
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 8000)) # 127.0.0.1
    print("Server Listening")
    server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    connection = server_socket.accept()[0].makefile('wb')
    try:
        print('Starting recording')
        camera.start_recording(connection, format='h264')
        camera.wait_recording(10)
        print('Stopping recording')
        camera.stop_recording()
    finally:
        connection.close()
        server_socket.close()
