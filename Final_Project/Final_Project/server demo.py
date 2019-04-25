import socket
import pyaudio
import wave
FORMAT=pyaudio.paInt16
FSAMP = 22050
FRAME_SIZE = 2048
p = pyaudio.PyAudio()
server=socket.socket()
server.bind(('0.0.0.0',8000))
server.listen(10)
(clientSocket,clientAddress)=server.accept()
stream = p.open(format=FORMAT,
                channels=1,
                rate=FSAMP,
                output=True)

stream.start_stream() 
l = clientSocket.recv(2048)
frames=[]
while(l):
    if l == "ClientSentToServer":
        break
    stream.write(l)
    l = clientSocket.recv(2048)

stream.stop_stream()
stream.close()

