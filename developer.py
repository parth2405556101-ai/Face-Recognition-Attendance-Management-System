from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2





class Developer:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root,text="DEVELOPER",
                            font=("Times New Roman",35,"bold"),
                            bg="white",fg="green",bd=4,relief=RIDGE)
        title_lbl.place(x=0,y=0,width=1530,height=45)

            # top image
        img_top = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image7.jpg")
        img_top = img_top.resize((1530,720), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=1530,height=720)

        #frame
        main_frame=Frame(f_lbl,bd=2,bg="white")
        main_frame.place(x=1000,y=0,width=500,height=720)

        
        # ---------- Developer 1 ----------
        img_top1 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image11.jpg")
        img_top1 = img_top1.resize((170, 170), Image.LANCZOS)
        self.photoimg_top1 = ImageTk.PhotoImage(img_top1)
        lbl1 = Label(main_frame,image=self.photoimg_top1)
        lbl1.place(x=300,y=5,width=170,height=170)

        dev_label = Label(
            main_frame, text="Parth Paliwal",
            font=("times new roman", 20, "bold"), bg="white"
        )
        dev_label.place(x=0,y=75)

        # ---------- Developer 2 ----------
        img_top2 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image13.jpg")
        img_top2 = img_top2.resize((170, 170), Image.LANCZOS)
        self.photoimg_top2 = ImageTk.PhotoImage(img_top2)
        lbl2 = Label(main_frame,image=self.photoimg_top2)
        lbl2.place(x=300,y=185,width=170,height=170)

        dev_label1 = Label(
            main_frame, text="Harshal Nivate",
            font=("times new roman", 20, "bold"), bg="white"
        )
        dev_label1.place(x=0,y=255)

        # ---------- Developer 3 ----------
        img_top3 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image10.jpg")
        img_top3 = img_top3.resize((170, 170), Image.LANCZOS)
        self.photoimg_top3 = ImageTk.PhotoImage(img_top3)
        lbl3 = Label(main_frame,image=self.photoimg_top3)
        lbl3.place(x=300,y=365,width=170,height=170)

        dev_label2 = Label(
            main_frame, text="Moksh Patel",
            font=("times new roman", 20, "bold"), bg="white"
        )
        dev_label2.place(x=0,y=435)

        # ---------- Developer 4 ----------
        img_top4 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image12.jpg")
        img_top4 = img_top4.resize((170, 170), Image.LANCZOS)
        self.photoimg_top4 = ImageTk.PhotoImage(img_top4)
        lbl4 = Label(main_frame,image=self.photoimg_top4)
        lbl4.place(x=300,y=545,width=170,height=170)

        dev_label3 = Label(
            main_frame, text="Parth Nalang",
            font=("times new roman", 20, "bold"), bg="white"
        )
        dev_label3.place(x=0,y=615)

        

if __name__ == "__main__":
    root = Tk()
    obj = Developer(root)
    root.mainloop()