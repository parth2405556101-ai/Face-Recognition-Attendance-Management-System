from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import cv2
import os
import csv
import numpy as np


#  Helper: resolve a file path relative to THIS script's folder

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "Parth.csv")
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
CLASSIFIER_PATH = os.path.join(BASE_DIR, "classifier.xml")

#  DB helper – open once, reuse

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root123",
        database="face_recognition"
    )


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        title_lbl = Label(
            self.root, text="FACE RECOGNITION",
            font=("Times New Roman", 35, "bold"),
            bg="white", fg="green", bd=4, relief=RIDGE
        )
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # ── Try to load header images; fall back to plain colours ──
        self._load_images()

        # ── Face Recognition button ──
        b1 = Button(
            self.root, text="Face Recognition",
            font=("Segoe UI", 14, "bold"),
            bg="#0f4c81", fg="#ffffff", relief=FLAT, cursor="hand2",
            command=self.face_recog
        )
        b1.place(x=565, y=680, width=400, height=50)


    #  Load background image to cover the screen
    def _load_images(self):
        bg_image_path = r"C:\Users\ACER\OneDrive\Pictures\image9.avif"
        try:
            # Resize image to cover the entire window (1530x790)
            img = Image.open(bg_image_path).resize((1530, 790), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            lbl = Label(self.root, image=photo)
            lbl.image = photo          # keep reference
            lbl.place(x=0, y=0, width=1530, height=790)
            
            # Send the background image to the bottom layer so it doesn't cover the title or buttons
            lbl.lower()
        except Exception:
            pass  # image file not found – skip silently


   
    def mark_attendance(self, name, roll, dep):
        """Append a row to Parth.csv if this student hasn't been marked today."""
        today = datetime.now().strftime("%d/%m/%Y")

        # Ensure the CSV exists with a header row
        if not os.path.exists(CSV_PATH):
            with open(CSV_PATH, "w", newline="") as f:
                csv.writer(f).writerow(["AttendanceId","Name","Roll","Department","Time","Date","Status"])

        # Read existing entries
        with open(CSV_PATH, "r") as f:
            lines = f.readlines()

        # Check if this student is already marked TODAY

        already_marked = False
        target_name = str(name).strip().lower()
        for line in lines[1:]:          # skip header
            parts = line.strip().split(",")
            if len(parts) >= 6:
                if parts[1].strip().lower() == target_name and parts[5].strip() == today:
                    already_marked = True
                    break

        if not already_marked:
            now = datetime.now()
            time_str = now.strftime("%H:%M:%S")
            # count existing data rows to generate next ID
            with open(CSV_PATH, "r") as f:
                existing = [r for r in f.readlines() if r.strip() and r.strip().lower() != "attendanceid,name,roll,department,time,date,status"]
            att_id = len(existing) + 1
            with open(CSV_PATH, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([att_id, name, roll, dep, time_str, today, "Present"])
            print(f"[Attendance] Marked ID={att_id}: {name} | {roll} | {dep} | {time_str} | {today}")

   
    def face_recog(self):

        # --- check required files exist ---
        if not os.path.exists(CASCADE_PATH):
            messagebox.showerror("File Missing",
                                 f"Cascade file not found:\n{CASCADE_PATH}", parent=self.root)
            return
        if not os.path.exists(CLASSIFIER_PATH):
            messagebox.showerror("File Missing",
                                 f"Classifier file not found:\n{CLASSIFIER_PATH}\n"
                                 "Please train the model first.", parent=self.root)
            return

        # --- load models ---
        faceCascade = cv2.CascadeClassifier(CASCADE_PATH)
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read(CLASSIFIER_PATH)

        # --- FIX: open DB connection ONCE before the video loop ---
        try:
            conn = get_db_connection()
            my_cursor = conn.cursor(buffered=True)
        except Exception as e:
            messagebox.showerror("Database Error",
                                 f"Cannot connect to database:\n{str(e)}", parent=self.root)
            return

        # ── inner helpers ───────────────────────────────────────
        def draw_boundary(img, classifier, scaleFactor, minNeighbors, color):
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Detect multiple faces in the frame
            features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

            # Display face count to highlight multiple face detection
            cv2.putText(img, f"Faces Detected: {len(features)}", (20, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

            for (x, y, w, h) in features:
                face_roi = gray_image[y:y + h, x:x + w]
                face_color_roi = img[y:y + h, x:x + w]

               

                is_spoof = False
                spoof_reason = ""

                # 1. Blur Check (catches mostly low-quality paper photos)
                sharpness = cv2.Laplacian(face_roi, cv2.CV_64F).var()
                if sharpness < 40:  # Stricter threshold for blurriness
                    is_spoof = True
                    spoof_reason = "Blurry"

                # 2. Glare/Light Emission Check (catches phone screens reflecting light or overexposing)
                _, bright_mask = cv2.threshold(face_roi, 230, 255, cv2.THRESH_BINARY)
                glare_ratio = cv2.countNonZero(bright_mask) / (w * h)
                if glare_ratio > 0.05:  # Stricter threshold for screen glare
                    is_spoof = True
                    if not spoof_reason:
                        spoof_reason = "Screen Glare"

                # 3. Authentic Skin Color Check in YCrCb
                ycrcb = cv2.cvtColor(face_color_roi, cv2.COLOR_BGR2YCrCb)
                # Standard human skin color range in YCrCb:
                skin_mask = cv2.inRange(ycrcb, (0, 133, 77), (255, 173, 127))
                skin_ratio = cv2.countNonZero(skin_mask) / (w * h)

                if skin_ratio < 0.25:  # Stricter threshold for skin-color
                    is_spoof = True
                    if not spoof_reason:
                        spoof_reason = "Color Shift"

                if is_spoof:
                    # Draw red bounding box and mark as spoof
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    spoof_y = y - 10 if y > 20 else y + h + 25
                    cv2.putText(img, f"Spoof: {spoof_reason}", (x, spoof_y),
                                cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 0, 255), 2)
                    continue  # Skip database lookup and attendance for spoofed faces

                # Draw standard boundary color initially
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 3)

                id_, predict = clf.predict(face_roi)
                confidence = int(100 * (1 - predict / 300))

                # ── Fetch student data using parameterised query ──
                try:
                    my_cursor.execute(
                        "SELECT Name, Roll, Dep FROM student WHERE Student_id = %s", (str(id_),)
                    )
                    result = my_cursor.fetchone()
                except Exception as db_err:
                    print("DB query error:", db_err)
                    result = None

                if result:
                    student_name, student_roll, student_dep = result
                else:
                    student_name, student_roll, student_dep = "Unknown", "N/A", "N/A"

                if confidence > 77:
                    # ── draw green box for known face ──
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    
                    # Ensure text stays within frame
                    if y < 80:
                        text_y = y + h + 45
                        dy = 25
                    else:
                        text_y = y - 55
                        dy = 25
                        
                    cv2.putText(img, f"Name: {student_name}",       (x, text_y),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Roll: {student_roll}",        (x, text_y + dy),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Department: {student_dep}",   (x, text_y + dy*2),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 2)
                    cv2.putText(img, f"Confidence: {confidence}% (Real)",   (x, y + h + 25),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)

                    # ── Pass correct variables to mark_attendance ──
                    self.mark_attendance(student_name, student_roll, student_dep)

                else:
                    # ── draw red box for unknown real face ──
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    unknown_y = y - 10 if y > 20 else y + h + 25
                    cv2.putText(img, "Unknown Face", (x, unknown_y),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                    cv2.putText(img, f"Conf: {confidence}%", (x, unknown_y + 25),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 255), 2)

            # Return the annotated img
            return img

        def recognize(img):
            # recognize() now returns the annotated frame correctly
            return draw_boundary(img, faceCascade, 1.1, 5, (255, 25, 255))

        # ── video loop ──────────────────────────────────────────
        video_cap = cv2.VideoCapture(0)
        if not video_cap.isOpened():
            messagebox.showerror("Camera Error",
                                 "Cannot open webcam. Check if it is connected.", parent=self.root)
            conn.close()
            return

        print("[Face Recognition] Camera opened. Press Enter to stop.")

        while True:
            ret, img = video_cap.read()
            if not ret:
                print("[Face Recognition] Frame read failed.")
                break

            img = recognize(img)
            cv2.imshow("Face Recognition – Press Enter to Exit", img)

            if cv2.waitKey(1) == 13:   # Enter key
                break

        video_cap.release()
        cv2.destroyAllWindows()
        conn.close()
        print("[Face Recognition] Session ended.")


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
