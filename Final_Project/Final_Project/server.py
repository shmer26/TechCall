import socket, videosocket
from check1 import VideoFeed
from Tkinter import *
from tkinter1 import Video_Stream
#from chat_server import App
from PIL import Image as Image
from PIL import ImageTk
import cv2
import tkMessageBox
from threading import Thread
import time


class Server:
    def __init__(self, root):
        self.root = root
        self.a = Video_Stream(self.root)
        self.root.protocol("WM_DELETE_WINDOW", self.Quit)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", 5999))
        self.server_socket.listen(5)
        self.videofeed = VideoFeed(1,"server",1)
        print "TCPServer Waiting for client on port 6000"
        client_socket, self.address = self.server_socket.accept()
        self.vsock = videosocket.videosocket(client_socket)
        self.send = Thread(target = self.send_frame)
        self.recv = Thread(target = self.recv_frame)

    def send_frame(self):
        while True:
            frame = self.videofeed.get_frame()
            self.vsock.vsend(frame)

    def recv_frame(self):
        while True:
            frame = self.vsock.vreceive()
            self.a.start(frame)

    def start(self):

        self.recv.start()
        time.sleep(1)
        self.send.start()

        #while 1:
            #client_socket, address = self.server_socket.accept()
        #print "I got a connection from ", self.address
            #vsock = videosocket.videosocket(client_socket)
        #frame=self.videofeed.get_frame()
        #self.vsock.vsend(frame)
        #frame=self.vsock.vreceive()
        #self.a.start(frame)
        #self.root.after(1,self.start)

    def Quit(self): #make sure the controller want to close the app
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.videofeed.CloseCam()#make everything stop
            self.root.destroy()#close the gui
            self.vsock.vclose()
                

if __name__ == "__main__":
    root = Tk()
    
    #app = App(root).start()
    server = Server(root)
    server.start()
    root.mainloop()


