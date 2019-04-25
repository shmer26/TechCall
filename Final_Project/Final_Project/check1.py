import cv2
import numpy
import io
from Tkinter import *
from PIL import Image
from PIL import ImageTk

class VideoFeed:

    def __init__(self,mode=1,name="w1",capture=1):
        print name
        self.camera_index = 0
        self.name = name
        self.cam = cv2.VideoCapture(self.camera_index)

    def get_frame(self):
        ret_val, img = self.cam.read()
        c = cv2.waitKey(1)
        if (c == "n"): #in "n" key is pressed while the popup window is in focus
            self.camera_index += 1 #try the next camera index
            self.cam = cv2.VideoCapture(self.camera_index)
            if not self.cam: #if the next camera index didn't work, reset to 0.
                self.camera_index = 0
                self.cam = cv2.VideoCapture(self.camera_index)

        #cv2.imshow('my webcam', img)
        cv2_im = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im)
        b = io.BytesIO()
        pil_im.save(b, 'jpeg')
        im_bytes = b.getvalue()
        return im_bytes

    def set_frame(self, frame_bytes):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        cv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_BGR2RGB)
        #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk

    def CloseCam(self):
        self.cam.release()
if __name__=="__main__":
    vf = VideoFeed(1,"test",1)
    while 1:
        m = vf.get_frame()
        a = vf.set_frame(m)
