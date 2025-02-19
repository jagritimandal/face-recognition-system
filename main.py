from tkinter import Label,Button,Tk,Frame
from PIL import Image,ImageTk
import os
from window_manager import open_train_window,open_student_window,open_face_window,open_update_window
#from tkinter import ttk

class Face_Recognition_System:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recogniton System")

        #bg img
        img1=Image.open(r"bg.png")
        img1=img1.resize((1530,710),Image.Resampling.LANCZOS)
        self.photoimg1=ImageTk.PhotoImage(img1)
        bg_img=Label(self.root,image=self.photoimg1)
        bg_img.place(x=0,y=0,width=1530,height=710)

        #title
        title_lbl=Label(text="Student Attendance System ",font=("times new roman",15,"bold"),bg="darkblue",fg="whitesmoke")
        title_lbl.place(x=0,y=1,width=330,height=35)

        frame = Frame(root, width=300, height=850, bg='darkblue')
        frame.place(x=5, y=45)
        
        #Student button1
        b1_1=Button(text="STUDENT DETAILS",cursor="hand2",command=self.go_to_student,font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b1_1.place(x=30,y=100,width=200,height=40)

        #Train data button5 
        b1_1=Button(text="TRAIN DATA",command=self.train_data,cursor="hand2",font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b1_1.place(x=30,y=150,width=200,height=40)

        #Detect face button 2
        b1_1=Button(text="DETECT FACE",command=self.face_data,cursor="hand2",font=("times new roman",10,"bold"),bg='skyblue',fg='black')
        b1_1.place(x=30,y=200,width=200,height=40)
        
        #Attendance face button3
        b1_1=Button(frame,text="ATTENDENCE MARKING",command=self.Attendence_print,cursor="hand2",font=("times new roman",10,"bold"),bg='skyblue',fg='black')
        b1_1.place(x=28,y=250,width=200,height=40)

        #Help button4
        b1_1=Button(text="HELP",cursor="hand2",font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b1_1.place(x=30,y=250,width=200,height=40)

        #Photos button6 
        b1_1=Button(text="PHOTOS",command=self.open_img,cursor="hand2",font=("times new roman",10,"bold"),bg="skyblue",fg="black")
        b1_1.place(x=30,y=350,width=200,height=40)

        frame = Frame(root, width=1000, height=700, bg='darkblue')
        frame.place(x=340, y=35)

        #first img
        img = Image.open(r"bg.png")
        img = img.resize((900, 700), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=350, y=40, width=900, height=700)
        
    def open_img(self):
        os.startfile("datasets")

#==========Functions button============

    def go_to_student(self):
        open_student_window(self.root)
    def train_data(self):
        open_train_window(self.root)
    def face_data(self):
        open_face_window(self.root)
    def Attendence_print(self):
        open_update_window(self.root)


if __name__=="__main__":
    root=Tk()
    obj=Face_Recognition_System(root)
    root.mainloop()