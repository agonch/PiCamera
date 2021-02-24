import socket
import time
import picamera
import subprocess

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False
while not connected:
    try:
        print("Trying connection...")
        client_socket.connect(('localhost', 8000))
        connected = True
    except Exception as _e:
        time.sleep(2)

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    # Run a viewer with an appropriate command line. Uncomment the mplayer
    # version if you would prefer to use mplayer instead of VLC
    # cmdline = ['vlc', '--demux', 'h264', '--h264-fps=50', '-']
    cmdline = ['mplayer', '-fps', '30', '-cache', '1024', '-framedrop', '-']
    player = subprocess.Popen(cmdline, stdin=subprocess.PIPE)
    while True:
        # Repeatedly read 1k of data from the connection and write it to
        # the media player's stdin
        data = connection.read(1024)
        if not data:
            break
        player.stdin.write(data)
finally:
    connection.close()
    client_socket.close()
    player.terminate()
