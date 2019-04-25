from Tkinter import *
from PIL import ImageTk, Image
import cv2 , numpy , io



class Video_Stream:
    def __init__(self,root,frame):
        self.root = root
        self.frame = frame
        # Create a frame
        app = Frame(root)
        app.place(x=0,y=0)
        # Create a label in the frame
        self.lmain = Label(app)
        
        # Capture from camera
        #self.cap = cv2.VideoCapture(0)
        
    # function for video streaming
    def start(self):
        #_, frame = self.cap.read()
        pil_bytes = io.BytesIO(self.frame)
        pil_image = Image.open(pil_bytes)
        cv2image = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image = img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image = imgtk)
        self.lmain.place(x=0,y=0)
        #self.lmain.after(1,self.start)
        
        
if __name__ == "__main__":
    #video_stream()
    root = Tk()
    root.geometry('1000x1000')
    c=Video_Stream(root, frame)
    c.start()
    root.mainloop()


