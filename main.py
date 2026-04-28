from tkinter import *
from PIL import Image, ImageTk
from student import Student
import os
from train import Train
from face_recognition import Face_Recognition
from attendance import Attendance
from developer import Developer
from email_sender import EmailSender

class Face_Recognition_System:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="#f0f2f7")

# ================= HEADER IMAGES =================

        img = Image.open(r"C:\Users\ACER\OneDrive\Pictures\0_Q2jXRZXXzEq2klcb.webp")
        img = img.resize((510,130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=510,height=130)


        img1 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\BarbaraCristina_300301L_image2-1024x264.jpg")
        img1 = img1.resize((510,130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl1 = Label(self.root,image=self.photoimg1)
        f_lbl1.place(x=510,y=0,width=510,height=130)


        img2 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\face-recognition-1024x630.jpg")
        img2 = img2.resize((510,130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl2 = Label(self.root,image=self.photoimg2)
        f_lbl2.place(x=1020,y=0,width=510,height=130)

# ================= BACKGROUND =================

        img3 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\istockphoto-2149530993-612x612.jpg")
        img3 = img3.resize((1530,660), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img = Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=660)

# ================= TITLE =================

        title_lbl = Label(bg_img,text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE",
                          font=("Segoe UI",30,"bold"),
                          bg="#ffffff",fg="#0f4c81",bd=4,relief=RIDGE)

        title_lbl.place(x=0,y=0,width=1530,height=50)

# ================= STUDENT BUTTON =================

        img_student = Image.open(r"C:\Users\ACER\OneDrive\Pictures\1000_F_206688661_kWRMFbjnF6h6T3fdiFHehxh3tmwd7cYh.jpg")
        img_student = img_student.resize((220,220), Image.LANCZOS)
        self.student_img = ImageTk.PhotoImage(img_student)

        b1 = Button(bg_img,image=self.student_img,command=self.student_details,cursor="hand2")
        b1.place(x=200,y=100,width=220,height=220)

        b1_1 = Button(bg_img,text="Student Details",
                      font=("Segoe UI",14,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",command=self.student_details)
        b1_1.place(x=200,y=300,width=220,height=40)

       

# ================= FACE DETECTOR =================

        img_face = Image.open(r"C:\Users\ACER\OneDrive\Pictures\images.jpeg")
        img_face = img_face.resize((220,220), Image.LANCZOS)
        self.face_img = ImageTk.PhotoImage(img_face)

        b2 = Button(bg_img,image=self.face_img,cursor="hand2",command=self.face_data)
        b2.place(x=500,y=100,width=220,height=220)

        b2_1 = Button(bg_img,text="Face Recognition",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",command=self.face_data)
        b2_1.place(x=500,y=300,width=220,height=40)

# ================= ATTENDANCE =================

        img_att = Image.open(r"C:\Users\ACER\OneDrive\Pictures\attendance-concept-businessman-holding-document-vector-flat-design-man-hold-clipboard-checklist-questionnaire-survey-task-155761789.webp")
        img_att = img_att.resize((220,220), Image.LANCZOS)
        self.att_img = ImageTk.PhotoImage(img_att)

        b3 = Button(bg_img,image=self.att_img,cursor="hand2",command=self.attendance_data)
        b3.place(x=800,y=100,width=220,height=220)

        b3_1 = Button(bg_img,text="Attendance",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",command=self.attendance_data)
        b3_1.place(x=800,y=300,width=220,height=40)

# ================= TRAIN DATA =================

        img_train = Image.open(r"C:\Users\ACER\OneDrive\Pictures\machine-learning-data-training-icon-vector-50041890.jpg")
        img_train = img_train.resize((220,220), Image.LANCZOS)
        self.train_img = ImageTk.PhotoImage(img_train)

        b4 = Button(bg_img,image=self.train_img,cursor="hand2",command=self.train_data)
        b4.place(x=1100,y=100,width=220,height=220)

        b4_1 = Button(bg_img,text="Train Data",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",command=self.train_data)
        b4_1.place(x=1100,y=300,width=220,height=40)

# ================= PHOTOS =================

        img_photos = Image.open(r"C:\Users\ACER\OneDrive\Pictures\vector-avatar-profile-icon-set-set-people-icons-flat-abstract-49809512.webp")
        img_photos = img_photos.resize((220,220), Image.LANCZOS)
        self.photos_img = ImageTk.PhotoImage(img_photos)

        b5 = Button(bg_img,image=self.photos_img,cursor="hand2",command=self.open_img)
        b5.place(x=200,y=380,width=220,height=220)

        b5_1 = Button(bg_img,text="Photos",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",command=self.open_img)
        b5_1.place(x=200,y=580,width=220,height=40)

# ================= DEVELOPER =================

        img_dev = Image.open(r"C:\Users\ACER\OneDrive\Pictures\gettyimages-1919380225-612x612.jpg")
        img_dev = img_dev.resize((220,220), Image.LANCZOS)
        self.dev_img = ImageTk.PhotoImage(img_dev)

        b6 = Button(bg_img,image=self.dev_img,cursor="hand2",command=self.developer_data)
        b6.place(x=500,y=380,width=220,height=220)

        b6_1 = Button(bg_img,text="Developer",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",command=self.developer_data)
        b6_1.place(x=500,y=580,width=220,height=40)

# ================= HELP =================

        img_help = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image8.avif")
        img_help = img_help.resize((220,220), Image.LANCZOS)
        self.help_img = ImageTk.PhotoImage(img_help)

        b7 = Button(bg_img,image=self.help_img,cursor="hand2")
        b7.place(x=800,y=380,width=220,height=220)

        b7_1 = Button(bg_img,text="Email Sender",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",
                      command=self.email_sender_data)
        b7_1.place(x=800,y=580,width=220,height=40)
        b7.config(command=self.email_sender_data)

# ================= EXIT =================

        img_exit = Image.open(r"C:\Users\ACER\OneDrive\Pictures\3d-exit-emergency-button-icon-illustration-png.png")
        img_exit = img_exit.resize((220,220), Image.LANCZOS)
        self.exit_img = ImageTk.PhotoImage(img_exit)

        b8 = Button(bg_img,image=self.exit_img,cursor="hand2",command=root.destroy)
        b8.place(x=1100,y=380,width=220,height=220)

        b8_1 = Button(bg_img,text="Exit",
                      font=("Times New Roman",15,"bold"),
                      bg="#0f4c81",fg="#ffffff",relief=FLAT,cursor="hand2",
                      command=root.destroy)
        b8_1.place(x=1100,y=580,width=220,height=40)

    def open_img(self):
                os.startfile("data")


        # ================= FUNCTION FOR STUDENT BUTTON =================

    def student_details(self):
                new_window = Toplevel(self.root)
                self.app = Student(new_window)

   
    def train_data(self):
                new_window = Toplevel(self.root)
                self.app = Train(new_window)

    
    def face_data(self):
                new_window = Toplevel(self.root)
                self.app = Face_Recognition(new_window)

    def attendance_data(self):
                new_window = Toplevel(self.root)
                self.app = Attendance(new_window)

    def developer_data(self):
                new_window = Toplevel(self.root)
                self.app = Developer(new_window)

    def email_sender_data(self):
                new_window = Toplevel(self.root)
                self.app = EmailSender(new_window)



    
         

if __name__ == "__main__":
    from login import run_login
    if run_login():
        root = Tk()
        obj = Face_Recognition_System(root)
        root.mainloop()
    else:
        print("Login cancelled.")