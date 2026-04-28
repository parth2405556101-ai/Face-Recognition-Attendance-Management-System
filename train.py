from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
import mysql.connector
import cv2
import os
import numpy as np






class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root,text="TRAIN DATA SET",
                          font=("Times New Roman",35,"bold"),
                          bg="white",fg="green",bd=4,relief=RIDGE)
        title_lbl.place(x=0,y=0,width=1530,height=45)

        # top image
        img_top = Image.open(r"C:\Users\ACER\OneDrive\Pictures\Untitled-design-45-1050x550.png")
        img_top = img_top.resize((1530,325), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        f_lbl = Label(self.root,image=self.photoimg_top)
        f_lbl.place(x=0,y=55,width=1530,height=325)

        # button
        b1 = Button(self.root,text="TRAIN DATA",cursor="hand2",
                    font=("Times New Roman",15,"bold"),bg="darkblue",fg="white",
                    command=self.train_classifier)
        b1.place(x=0,y=380,width=1530,height=60)

        # bottom image
        img_bottom = Image.open(r"C:\Users\ACER\OneDrive\Pictures\images3.avif")
        img_bottom = img_bottom.resize((1530,325), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        f_lbl = Label(self.root,image=self.photoimg_bottom)
        f_lbl.place(x=0,y=440,width=1530,height=325)

    def train_classifier(self):
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.exists(data_dir):
            messagebox.showerror("Error", "Data directory not found: data/", parent=self.root)
            return

        images = []
        for root, _, files in os.walk(data_dir):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.pgm', '.bmp')):
                    images.append(os.path.join(root, file))

        if len(images) == 0:
            messagebox.showerror("Error", "No training images found in data/", parent=self.root)
            return

        faces = []
        ids = []

        for image_path in images:
            try:
                img = Image.open(image_path).convert("L")
            except Exception as ex:
                print("Skipping", image_path, ex)
                continue

            imageNp = np.array(img, 'uint8')

            import re as _re
            file_name = os.path.basename(image_path)
            name_no_ext = os.path.splitext(file_name)[0]
            parts = name_no_ext.split('.')
            id_ = None
            if parts[0].lower() == 'user' and len(parts) >= 2 and parts[1].isdigit():
                id_ = int(parts[1])
            elif parts[0].isdigit():
                id_ = int(parts[0])
            else:
                nums = _re.findall(r'\d+', name_no_ext)
                if nums:
                    id_ = int(nums[0])
            if id_ is None:
                pdir = os.path.basename(os.path.dirname(image_path))
                nums = _re.findall(r'\d+', pdir)
                id_ = int(nums[0]) if nums else 0
            print(f"[Train] {file_name} -> ID: {id_}")

            faces.append(imageNp)
            ids.append(id_)

            cv2.imshow("Training", imageNp)
            if cv2.waitKey(1) == 13:
                break

        if len(faces) == 0:
            messagebox.showerror("Error", "No valid face images for training.", parent=self.root)
            return

        try:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
        except AttributeError:
            messagebox.showerror("Error", "cv2.face module not available. Install opencv-contrib-python.", parent=self.root)
            return

        # ensure ids is int32 — required by LBPH
        ids = np.array(ids, dtype=np.int32)
        recognizer.train(faces, ids)
        model_path = os.path.join(os.getcwd(), "classifier.xml")
        recognizer.write(model_path)

        cv2.destroyAllWindows()
        messagebox.showinfo("Result", f"Training completed successfully! Model saved: {model_path}")






if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()