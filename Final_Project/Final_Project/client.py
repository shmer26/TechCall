import socket, videosocket
import StringIO
#from chat_client import App
from check1 import VideoFeed
import sys
from Tkinter import *
from tkinter1 import Video_Stream

class Client:
    def __init__(self,root ,ip_addr = "10.0.0.14"):
        self.root = root
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(('10.0.0.3', 6007))
        self.vsock = videosocket.videosocket (self.client_socket)
        self.videofeed = VideoFeed(1,"client",1)
        self.data = StringIO.StringIO()

    def connect(self):
        while True:
            frame=self.videofeed.get_frame()
            self.vsock.vsend(frame)
            frame = self.vsock.vreceive()
            a = Video_Stream(root,frame)
            a.start()
            root.mainloop()
            
            
if __name__ == "__main__":
    global root
    root = Tk()
    #app = App(master).start()
    ip_addr = "10.0.0.14"
    if len(sys.argv) == 2:
        ip_addr = sys.argv[1]

    print "Connecting to " + ip_addr + "...."
    client = Client(root, ip_addr)
    client.connect()

