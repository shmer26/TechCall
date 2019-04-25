import socket, videosocket
from check1 import VideoFeed
from Tkinter import *
from tkinter1 import Video_Stream
#from chat_server import App
from PIL import Image as Image
from PIL import ImageTk
import cv2
import tkMessageBox


class Server:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.Quit)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", 5999))
        self.server_socket.listen(5)
        self.videofeed = VideoFeed(1,"server",1)
        print "TCPServer Waiting for client on port 6000"
        client_socket, self.address = self.server_socket.accept()
        self.vsock = videosocket.videosocket(client_socket)



    def start(self):
        #while 1:
            #client_socket, address = self.server_socket.accept()
        print "I got a connection from ", self.address
            #vsock = videosocket.videosocket(client_socket)
        frame=self.videofeed.get_frame()
        self.vsock.vsend(frame)
        frame=self.vsock.vreceive()
        a = Video_Stream(self.root,frame)
        a.start()
        self.root.after(1,self.start)

    def Quit(self): #make sure the controller want to close the app
        if tkMessageBox.askokcancel("Quit", "Do you really wish to quit?"):
            self.videofeed.CloseCam()#make everything stop
            self.root.destroy()#close the gui
            self.vsock.vclose()
                

if __name__ == "__main__":
    global root
    root = Tk()
    
    #app = App(root).start()
    server = Server(root)
    server.start()
    root.mainloop()


