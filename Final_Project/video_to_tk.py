import cv2
import numpy
import io
from tkinter1 import Video_Stream
from Tkinter import *
from PIL import Image
from PIL import ImageTk



'''
def set_frame(self, frame_bytes):
        pil_bytes = io.BytesIO(frame_bytes)
        pil_image = Image.open(pil_bytes)
        cv_image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
        #cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv_image)
        imgtk = ImageTk.PhotoImage(image=img)
        return imgtk
'''

root = Tk()
a=Video_Stream(root)
a.start()
root.mainloop()
