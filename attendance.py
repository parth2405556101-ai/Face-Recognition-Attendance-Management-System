from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import os
import csv
from tkinter import filedialog

mydata = []

class Attendance:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        # header images
        try:
            img = Image.open(r"C:\Users\ACER\OneDrive\Pictures\0_Q2jXRZXXzEq2klcb.webp")
            img = img.resize((800, 200), Image.LANCZOS)
            self.photoimg = ImageTk.PhotoImage(img)
            Label(self.root, image=self.photoimg).place(x=0, y=0, width=800, height=200)
        except Exception: pass

        try:
            img1 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\image6.jpg")
            img1 = img1.resize((800, 200), Image.LANCZOS)
            self.photoimg1 = ImageTk.PhotoImage(img1)
            Label(self.root, image=self.photoimg1).place(x=800, y=0, width=800, height=200)
        except Exception: pass

        try:
            img2 = Image.open(r"C:\Users\ACER\OneDrive\Pictures\istockphoto-2149530993-612x612.jpg")
            img2 = img2.resize((1530, 660), Image.LANCZOS)
            self.photoimg2 = ImageTk.PhotoImage(img2)
            bg_img = Label(self.root, image=self.photoimg2)
        except Exception:
            bg_img = Label(self.root, bg="#f0f0f0")
        bg_img.place(x=0, y=200, width=1530, height=660)

        title_lbl = Label(bg_img, text="ATTENDANCE MANAGEMENT SYSTEM",
                          font=("Times New Roman", 35, "bold"),
                          bg="white", fg="green", bd=4, relief=RIDGE)
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1500, height=600)

        # ── Left frame ─────────────────────────────────────────
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                text="Student Attendance Details",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=580)

        try:
            img_left = Image.open(r"C:\Users\ACER\OneDrive\Pictures\images (1).jpeg")
            img_left = img_left.resize((720, 130), Image.LANCZOS)
            self.photoimg_left = ImageTk.PhotoImage(img_left)
            Label(Left_frame, image=self.photoimg_left).place(x=5, y=0, width=720, height=130)
        except Exception: pass

        left_inside_frame = Frame(Left_frame, bd=2, relief=RAISED, bg="white")
        left_inside_frame.place(x=0, y=135, width=720, height=370)

        # ── All variables including var_id ─────────────────────
        self.var_id                = StringVar()
        self.var_roll              = StringVar()
        self.var_name              = StringVar()
        self.var_dep               = StringVar()
        self.var_time              = StringVar()
        self.var_date              = StringVar()
        self.var_attendance_status = StringVar()

        # ── Form fields ────────────────────────────────────────
        Label(left_inside_frame, text="Attendance ID:", font=("times new roman",12,"bold"), bg="white").grid(row=0,column=0,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_id,   width=20, font=("times new roman",12,"bold"), state="readonly").grid(row=0,column=1,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Name:",         font=("times new roman",12,"bold"), bg="white").grid(row=0,column=2,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_name, width=20, font=("times new roman",12,"bold")).grid(row=0,column=3,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Roll:",         font=("times new roman",12,"bold"), bg="white").grid(row=1,column=0,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_roll, width=20, font=("times new roman",12,"bold")).grid(row=1,column=1,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Department:",   font=("times new roman",12,"bold"), bg="white").grid(row=1,column=2,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_dep,  width=20, font=("times new roman",12,"bold")).grid(row=1,column=3,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Time:",         font=("times new roman",12,"bold"), bg="white").grid(row=2,column=0,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_time, width=20, font=("times new roman",12,"bold")).grid(row=2,column=1,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Date:",         font=("times new roman",12,"bold"), bg="white").grid(row=2,column=2,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_date, width=20, font=("times new roman",12,"bold")).grid(row=2,column=3,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Attendance Status:", font=("times new roman",12,"bold"), bg="white").grid(row=3,column=0,padx=10,pady=6,sticky=W)
        self.atten_status = ttk.Combobox(left_inside_frame, textvariable=self.var_attendance_status,
                                         font=("times new roman",12,"bold"), state="readonly", width=20)
        self.atten_status["values"] = ("Status", "Present", "Absent")
        self.atten_status.current(0)
        self.atten_status.grid(row=3, column=1, padx=10, pady=6, sticky=W)

        # ── Buttons ────────────────────────────────────────────
        btn_frame = Frame(left_inside_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=210, width=715, height=35)

        Button(btn_frame, text="Import csv", command=self.import_csv, width=17,
               font=("times new roman",13,"bold"), bg="blue",   fg="white").grid(row=0, column=0)
        Button(btn_frame, text="Export csv", command=self.export_csv, width=17,
               font=("times new roman",13,"bold"), bg="blue",   fg="white").grid(row=0, column=1)
        Button(btn_frame, text="Update",     command=self.update_data, width=17,
               font=("times new roman",13,"bold"), bg="green",  fg="white").grid(row=0, column=2)
        Button(btn_frame, text="Reset",      command=self.reset_data,  width=17,
               font=("times new roman",13,"bold"), bg="orange", fg="white").grid(row=0, column=3)

        # ── Right frame ────────────────────────────────────────
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 text="Attendance Details",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=720, height=580)

        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=700, height=650)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.AttendanceReportTable = ttk.Treeview(table_frame,
            columns=("id", "name", "roll", "department", "time", "date", "status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)

        self.AttendanceReportTable.heading("id",         text="AttendanceId")
        self.AttendanceReportTable.heading("name",       text="Name")
        self.AttendanceReportTable.heading("roll",       text="Roll")
        self.AttendanceReportTable.heading("department", text="Department")
        self.AttendanceReportTable.heading("time",       text="Time")
        self.AttendanceReportTable.heading("date",       text="Date")
        self.AttendanceReportTable.heading("status",     text="Attendance Status")

        self.AttendanceReportTable["show"] = "headings"

        self.AttendanceReportTable.column("id",         width=90)
        self.AttendanceReportTable.column("name",       width=110)
        self.AttendanceReportTable.column("roll",       width=70)
        self.AttendanceReportTable.column("department", width=100)
        self.AttendanceReportTable.column("time",       width=85)
        self.AttendanceReportTable.column("date",       width=95)
        self.AttendanceReportTable.column("status",     width=120)

        self.AttendanceReportTable.tag_configure("present", background="#e6f9ec")
        self.AttendanceReportTable.tag_configure("absent",  background="#fde8e8")

        self.AttendanceReportTable.pack(fill=BOTH, expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>", self.get_cursor)

    # ── fetch_data ─────────────────────────────────────────────
    def fetch_data(self, rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            if not any(str(c).strip() for c in i):
                continue
            first = str(i[0]).strip().lower()
            if first in ("attendanceid", "name", "id"):
                continue
            if len(i) >= 7:
                row_vals = tuple(i[:7])
                status   = str(i[6]).strip()
            elif len(i) == 6:
                row_vals = ("—",) + tuple(i[:6])
                status   = str(i[5]).strip()
            else:
                continue
            tag = "present" if status.lower() == "present" else "absent"
            self.AttendanceReportTable.insert("", END, values=row_vals, tags=(tag,))

    # ── get_cursor: click row → fill fields ────────────────────
    def get_cursor(self, event=""):
        f = self.AttendanceReportTable.focus()
        d = self.AttendanceReportTable.item(f)["values"]
        if not d or len(d) < 7:
            return
        self.var_id.set(d[0])
        self.var_name.set(d[1])
        self.var_roll.set(d[2])
        self.var_dep.set(d[3])
        self.var_time.set(d[4])
        self.var_date.set(d[5])
        self.var_attendance_status.set(d[6])

    # ── update_data: edit selected row in CSV ──────────────────
    def update_data(self):
        att_id = str(self.var_id.get()).strip()
        if not att_id or att_id == "—":
            messagebox.showerror("Error", "Please select a row from the table first.", parent=self.root)
            return
        if self.var_attendance_status.get() == "Status":
            messagebox.showerror("Error", "Please select an Attendance Status.", parent=self.root)
            return
        if not mydata:
            messagebox.showerror("Error", "No data loaded. Import CSV first.", parent=self.root)
            return

        updated = False
        for i, row in enumerate(mydata):
            if not row or str(row[0]).strip().lower() in ("attendanceid","id"):
                continue
            if str(row[0]).strip() == att_id:
                mydata[i] = [
                    att_id,
                    self.var_name.get(),
                    self.var_roll.get(),
                    self.var_dep.get(),
                    self.var_time.get(),
                    self.var_date.get(),
                    self.var_attendance_status.get()
                ]
                updated = True
                break

        if updated:
            # Save back to the same CSV file
            try:
                fln = filedialog.asksaveasfilename(
                    initialdir=os.getcwd(), title="Save updated CSV",
                    defaultextension=".csv",
                    filetypes=(("CSV File","*.csv"),("All File","*.*")),
                    parent=self.root)
                if fln:
                    with open(fln, mode="w", newline="") as f:
                        csv.writer(f).writerows(mydata)
                    self.fetch_data(mydata)
                    messagebox.showinfo("Updated",
                        f"Attendance ID {att_id} updated and saved successfully.",
                        parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self.root)
        else:
            messagebox.showerror("Not Found",
                f"Attendance ID {att_id} not found in loaded data.", parent=self.root)

    # ── import / export ────────────────────────────────────────
    def import_csv(self):
        global mydata
        mydata.clear()
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Open CSV",
            filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
        if not fln:
            return
        with open(fln, newline="", encoding="utf-8-sig") as myfile:
            for row in csv.reader(myfile, delimiter=","):
                mydata.append(row)
        self.fetch_data(mydata)

    def export_csv(self):
        try:
            if not mydata:
                messagebox.showerror("No Data", "No data found to export.", parent=self.root)
                return
            fln = filedialog.asksaveasfilename(
                initialdir=os.getcwd(), title="Save CSV",
                defaultextension=".csv",
                filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
            if not fln:
                return
            with open(fln, mode="w", newline="") as myfile:
                csv.writer(myfile).writerows(mydata)
            messagebox.showinfo("Data Exported",
                "Exported to " + os.path.basename(fln) + " successfully.", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Due to {str(e)}", parent=self.root)

    # ── reset ──────────────────────────────────────────────────
    def reset_data(self):
        self.var_id.set("")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_dep.set("")
        self.var_time.set("")
        self.var_date.set("")
        self.var_attendance_status.set("Status")


if __name__ == "__main__":
    root = Tk()
    obj = Attendance(root)
    root.mainloop()
