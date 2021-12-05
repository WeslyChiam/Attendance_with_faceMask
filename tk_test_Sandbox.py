from tkinter import *
import tkinter as tk
import tkinter.font as font
from tkinter.ttk import Label
from PIL import ImageTk, Image
import cv2
import numpy as np
from keras.models import load_model
import os 
from datetime import datetime, timedelta
import time

class App(tk.Frame):
    #Widget Section 
   def __init__(self):
        self.root = tk.Tk()
        self.root.title("Human Flow Tracker")
        self.root.geometry("500x300")

        # Canvas 
        global canvas
        canvas = Canvas(width=300, height=300, bg="white")
        canvas.pack(expand=YES, fill=BOTH)

        # Library for Image Store
        stopImg = Image.open("./icon/stop_sign.gif")
        stopImg = stopImg.resize((100,100), Image.ANTIALIAS)
        stopPhoto = ImageTk.PhotoImage(stopImg)

        global warnImg
        warnSign = PhotoImage(file="./icon/warningSign.gif")
        warnSign = warnSign.subsample(8,8)
        warnImg = canvas.create_image(265,88, anchor=NW, image=warnSign)
        canvas.itemconfigure(warnImg, state='hidden')

        global timeWarnImg
        timeWarn = PhotoImage(file="./icon/timeWarningSign.gif")
        timeWarn = timeWarn.subsample(8,8)
        timeWarnImg = canvas.create_image(265,88, anchor=NW, image=timeWarn)
        canvas.itemconfigure(timeWarnImg, state='hidden')
        
       

        self.maxNumLabel = tk.Label(self.root, bg='white', text = "Maximum Number: ", font=("Arial",15))
        self.maxNumEntry = tk.Entry(self.root)
        self.submitButton = tk.Button(self.root, text="Submit", command=self.get)
        self.quitButton = tk.Button(self.root, text="Quit", command=self.root.destroy)
        self.saveLabel = tk.Label(self.root, bg='white', text  = "Press 'S' to save captured image from camera", font=("Arial", 15))
        self.quitLabel = tk.Label(self.root, bg='white', text  = "Press 'Q' to quit from the camera", font=("Arial", 15))
        # self.noteLabel = tk.Label(self.root, bg='white',
        #                      text  = "This program still unvailable to recognize people , manual save is require", 
        #                      font=("Arial", 15))
        self.backButton = tk.Button(self.root, text="Back", command=self.newScreen)
        self.alertLabel = tk.Label(self.root, bg='white', text = "Maximum Number Reached!", font=("Arial", 15))
        # self.imageLabel = tk.Label(self.root,image=stopPhoto)
        self.helpLabel1 = tk.Label(self.root, bg="white", 
                            text="This program capture each person by command and auto set on timer", 
                            font=("Arial", 10))
        self.helpLabel2 = tk.Label(self.root, bg="white", 
                            text="When the timer reach end, the program will alert user", 
                            font=("Arial", 10))
        self.helpLabel3 = tk.Label(self.root, bg="white", 
                            text="This program will prompt out new window for camera", 
                            font=("Arial", 10))
        self.helpLabel4 = tk.Label(self.root, bg="white", 
                            text="Press 'S' to save captured image from camera", 
                            font=("Arial", 10))
        self.helpLabel5 = tk.Label(self.root, bg="white", 
                            text="Press 'Q' to quit from the camera", 
                            font=("Arial", 10))
        self.aboutLabel = tk.Label(self.root, bg="white", 
                            text="This program is developed by Wesly Chiam Wei Lek",
                            font=("Arial", 13))
        self.contactLabel = tk.Label(self.root, bg="White",
                            text="Contact: chiamwesly@gmail.com",
                            font=("Arial", 12))

        # Menu Bar
        menu = Menu(self.root)
        self.root.config(menu=menu)
        file = Menu(menu, tearoff=0)
        file.add_command(label="Home", command=self.newScreen)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        help = Menu(menu, tearoff=0)
        help.add_command(label="Help", command=self.help_wind)
        help.add_command(label="About Us", command=self.about_windw)
        menu.add_cascade(label="Help", menu=help)

        self.maxNumLabel.place(x=1,y=1)
        self.maxNumEntry.place(x=1,y=30)
        self.submitButton.place(x=1,y=50)
        self.quitButton.place(x=60,y=50)
        self.saveLabel.place(x=1, y=75)
        self.quitLabel.place(x=1,y=100)
        
        self.root.mainloop()

    #Widget Function Section
   def get(self):
     maxNum = self.maxNumEntry.get()
     if (maxNum.isdigit()):
        maxNum = int(maxNum)
        self.maxNumLabel.config(text = "Capturing Image... Please do not turn off the window")
        self.cam(self, maxNum)
    
     else:
        self.maxNumEntry.delete(0,'end') 

   def maxNumAlertPop(self):
        self.root.title("WARNING")
        # self.root.geometry("700x300")
        self.submitButton.place_forget()
        self.maxNumEntry.place_forget()
        self.saveLabel.place_forget()
        self.quitLabel.place_forget()
        self.maxNumLabel.config(text = "Maximum Number Reached!")
        self.backButton.place(x=30,y=30)
        self.quitButton.place(x=90,y=30)
        canvas.itemconfigure(warnImg, state='normal')
        

   def maxTimeAlertPop(self):
    self.root.title("WARNING")
    # self.root.geometry("700x300")
    self.submitButton.place_forget()
    self.maxNumEntry.place_forget()
    self.saveLabel.place_forget()
    self.quitLabel.place_forget()
    self.maxNumLabel.config(text = "Time Limit Reached! Please inform people to leave")
    self.backButton.place(x=30,y=30)
    self.quitButton.place(x=90,y=30)
    # self.imageLabel.place(x=70,y=10)
    canvas.itemconfigure(timeWarnImg, state='normal')

   def newScreen(self):
        canvas.itemconfigure(warnImg, state='hidden')
        canvas.itemconfigure(timeWarnImg, state='hidden')
        self.maxNumLabel.config(text="Maximum Number: ")
        self.maxNumEntry.place_forget()
        self.submitButton.place_forget()
        self.backButton.place_forget()
        self.quitButton.place_forget()
        self.saveLabel.place_forget()
        self.quitLabel.place_forget()
        self.helpLabel1.place_forget()
        self.helpLabel2.place_forget()
        self.helpLabel3.place_forget()
        self.helpLabel4.place_forget()
        self.helpLabel5.place_forget()
        self.aboutLabel.place_forget()
        self.contactLabel.place_forget()
        self.maxNumEntry.place(x=1,y=30)
        self.submitButton.place(x=1,y=50)
        self.quitButton.place(x=60,y=50)
        self.saveLabel.place(x=1, y=75)
        self.quitLabel.place(x=1,y=100)

   def about_windw(self):
        canvas.itemconfigure(warnImg, state='hidden')
        canvas.itemconfigure(timeWarnImg, state='hidden')
        self.maxNumLabel.config(text="About Us")
        self.maxNumEntry.place_forget()
        self.submitButton.place_forget()
        self.quitButton.place_forget()
        self.saveLabel.place_forget()
        self.quitLabel.place_forget()
        self.helpLabel1.place_forget()
        self.helpLabel2.place_forget()
        self.helpLabel3.place_forget()
        self.helpLabel4.place_forget()
        self.helpLabel5.place_forget()
        self.contactLabel.place_forget()
        self.aboutLabel.place(x=1,y=40)
        self.contactLabel.place(x=1, y=60)

   def help_wind(self):
        canvas.itemconfigure(warnImg, state='hidden')
        canvas.itemconfigure(timeWarnImg, state='hidden')
        self.maxNumLabel.config(text="Help")
        self.maxNumEntry.place_forget()
        self.submitButton.place_forget()
        self.quitButton.place_forget()
        self.saveLabel.place_forget()
        self.quitLabel.place_forget()
        self.aboutLabel.place_forget()
        self.contactLabel.place_forget()
        self.helpLabel1.place(x=1,y=30)
        self.helpLabel2.place(x=1,y=50)
        self.helpLabel3.place(x=1,y=70)
        self.helpLabel4.place(x=1,y=90)
        self.helpLabel5.place(x=1,y=110)

   def client_exit(self):
        exit()

# ML Recognised Live Section
   @staticmethod
   def cam(self, maxNum):
    print(maxNum)
    model=load_model("./model-010.h5")

    results={0:'mask',1:'without mask'}
    GR_dict={0:(0,255,0),1:(0,0,255)}

    rect_size = 4
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    count = 0
    amtCount = 0

    ListOfPeople = []

    haarcascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    while True:
        # print(len(ListOfPeople))
        (rval, im) = cap.read()
        im=cv2.flip(im,1,1) 

        #This part is to set up clock
        # global time
        # global FMT
        now = datetime.now()
        time = now.strftime("%H-%M-%S")
        date = now.strftime("%d-%m-%Y")
        tmpTime = now.strftime("%H:%M:%S")
        FMT = '%H-%M-%S'
        tmpStrTime = str(tmpTime)
        checkCam = None


        rerect_size = cv2.resize(im, (im.shape[1] // rect_size, im.shape[0] // rect_size))
        faces = haarcascade.detectMultiScale(rerect_size)
        for f in faces:
            (x, y, w, h) = [v * rect_size for v in f]
            roi_color = im[y:y+h, x:x+w]
            
            #Create image 
            face_img = im[y:y+h, x:x+w]
            rerect_sized=cv2.resize(face_img,(150,150))
            normalized=rerect_sized/255.0
            reshaped=np.reshape(normalized,(1,150,150,3))
            reshaped = np.vstack([reshaped])
            result=model.predict(reshaped)
            label=np.argmax(result,axis=1)[0]

            #Capture image once reach the count 
            if cv2.waitKey(1) & 0xFF == ord('s'):
                path = os.path.join("log/record/", date + "/")
                os.makedirs(path, exist_ok=True)
                log_img = os.path.join(path, time + ".jpg")
                cv2.imwrite(log_img, roi_color)
                ListOfPeople.append(time)
                count += 1
      
            cv2.rectangle(im,(x,y),(x+w,y+h),GR_dict[label],2)
            cv2.rectangle(im,(x,y-40),(x+w,y),GR_dict[label],-1)
            cv2.putText(im, results[label], (x, y-10),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2)

        cv2.imshow('Capturing Image...',   im)
        key = cv2.waitKey(1) & 0xFF

        # Use for loop for check min
        for checkMin in ListOfPeople:
         tdelta = datetime.strptime(time,FMT) - datetime.strptime(checkMin, FMT)
         strTdelta = str(tdelta)
         print(strTdelta)
         if strTdelta == "0:00:10":
          checkCam = True
          self.maxTimeAlertPop()
          print("Time's Up")
          break
          
        if checkCam:
            break

        if(len(ListOfPeople) == maxNum):
            self.maxNumAlertPop()
            break
                      
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

    cv2.destroyAllWindows()

app = App()












