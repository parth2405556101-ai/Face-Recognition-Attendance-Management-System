from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import mysql.connector
import os
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from collections import defaultdict
from datetime import datetime

mydata = []
DB = dict(host="localhost", user="root", password="root123", database="face_recognition")


class EmailSender:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.csv_data = []

        # ── Header images (same as attendance.py) ──────────────
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

        # ── Title (same style as attendance.py) ────────────────
        title_lbl = Label(bg_img, text="EMAIL SENDER — LOW ATTENDANCE ALERT",
                          font=("Times New Roman", 35, "bold"),
                          bg="white", fg="green", bd=4, relief=RIDGE)
        title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(bg_img, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1500, height=600)

        # ══════════════════════════════════════════════════════
        # LEFT FRAME — same structure as attendance.py left frame
        # ══════════════════════════════════════════════════════
        Left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                text="Email Configuration",
                                font=("times new roman", 12, "bold"))
        Left_frame.place(x=10, y=10, width=730, height=580)

        try:
            img_left = Image.open(r"C:\Users\ACER\OneDrive\Pictures\images (1).jpeg")
            img_left = img_left.resize((720, 130), Image.LANCZOS)
            self.photoimg_left = ImageTk.PhotoImage(img_left)
            Label(Left_frame, image=self.photoimg_left).place(x=5, y=0, width=720, height=130)
        except Exception: pass

        left_inside_frame = Frame(Left_frame, bd=2, relief=RAISED, bg="white")
        left_inside_frame.place(x=0, y=135, width=720, height=430)

        # ── Variables ──────────────────────────────────────────
        self.var_sender    = StringVar(value="parthpaliwal05@gmail.com")
        self.var_password  = StringVar(value="jnvgohlvnycskjwh")
        self.var_college   = StringVar(value="Vidyavardhini's College of Engineering and Technology")
        self.var_threshold = StringVar(value="75")
        self.var_csv_path  = StringVar(value="No file loaded")
        # selected row display
        self.var_name   = StringVar()
        self.var_roll   = StringVar()
        self.var_dep    = StringVar()
        self.var_pct    = StringVar()
        self.var_pemail = StringVar()

        # ── Form fields (same layout as attendance.py fields) ──
        Label(left_inside_frame, text="Sender Gmail:", font=("times new roman",12,"bold"), bg="white").grid(row=0,column=0,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_sender, width=25, font=("times new roman",12,"bold")).grid(row=0,column=1,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="App Password:", font=("times new roman",12,"bold"), bg="white").grid(row=0,column=2,padx=10,pady=6,sticky=W)
        self.pwd_entry = ttk.Entry(left_inside_frame, textvariable=self.var_password, width=18, font=("times new roman",12,"bold"), show="*")
        self.pwd_entry.grid(row=0, column=3, padx=10, pady=6, sticky=W)

        Label(left_inside_frame, text="College Name:", font=("times new roman",12,"bold"), bg="white").grid(row=1,column=0,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_college, width=25, font=("times new roman",12,"bold")).grid(row=1,column=1,padx=10,pady=6,sticky=W)

        Label(left_inside_frame, text="Threshold %:", font=("times new roman",12,"bold"), bg="white").grid(row=1,column=2,padx=10,pady=6,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_threshold, width=8, font=("times new roman",12,"bold")).grid(row=1,column=3,padx=10,pady=6,sticky=W)

        # Show password checkbox
        self.show_pwd_var = BooleanVar(value=False)
        def toggle_pwd():
            self.pwd_entry.config(show="" if self.show_pwd_var.get() else "*")
        Checkbutton(left_inside_frame, text="Show Password",
                    variable=self.show_pwd_var, command=toggle_pwd,
                    font=("times new roman",11), bg="white", cursor="hand2"
                    ).grid(row=2, column=0, columnspan=2, padx=10, sticky=W)

        Label(left_inside_frame, text="ℹ Use Gmail App Password (not regular password)",
              font=("times new roman",10,"italic"), bg="white", fg="gray"
              ).grid(row=2, column=2, columnspan=2, padx=10, sticky=W)

        # Selected student info (mirrors attendance fields)
        Label(left_inside_frame, text="Selected Name:", font=("times new roman",12,"bold"), bg="white").grid(row=3,column=0,padx=10,pady=4,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_name, width=20, font=("times new roman",12,"bold"), state="readonly").grid(row=3,column=1,padx=10,pady=4,sticky=W)

        Label(left_inside_frame, text="Roll:", font=("times new roman",12,"bold"), bg="white").grid(row=3,column=2,padx=10,pady=4,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_roll, width=18, font=("times new roman",12,"bold"), state="readonly").grid(row=3,column=3,padx=10,pady=4,sticky=W)

        Label(left_inside_frame, text="Department:", font=("times new roman",12,"bold"), bg="white").grid(row=4,column=0,padx=10,pady=4,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_dep, width=20, font=("times new roman",12,"bold"), state="readonly").grid(row=4,column=1,padx=10,pady=4,sticky=W)

        Label(left_inside_frame, text="Attendance%:", font=("times new roman",12,"bold"), bg="white").grid(row=4,column=2,padx=10,pady=4,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_pct, width=18, font=("times new roman",12,"bold"), state="readonly").grid(row=4,column=3,padx=10,pady=4,sticky=W)

        Label(left_inside_frame, text="Parent Email:", font=("times new roman",12,"bold"), bg="white").grid(row=5,column=0,padx=10,pady=4,sticky=W)
        ttk.Entry(left_inside_frame, textvariable=self.var_pemail, width=45, font=("times new roman",12,"bold"), state="readonly").grid(row=5,column=1,columnspan=3,padx=10,pady=4,sticky=W)

        # CSV path display
        Label(left_inside_frame, text="CSV File:", font=("times new roman",11,"bold"), bg="white").grid(row=6,column=0,padx=10,pady=4,sticky=W)
        Label(left_inside_frame, textvariable=self.var_csv_path, font=("times new roman",10), bg="white", fg="blue", wraplength=400).grid(row=6,column=1,columnspan=3,padx=10,sticky=W)

        # ── Buttons (same style as attendance.py) ─────────────
        btn_frame = Frame(left_inside_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=305, width=715, height=35)

        Button(btn_frame, text="Load CSV",        command=self.load_csv,      width=16,
               font=("times new roman",13,"bold"), bg="blue",   fg="white").grid(row=0, column=0)
        Button(btn_frame, text="Calculate",       command=self.calculate,     width=16,
               font=("times new roman",13,"bold"), bg="orange", fg="white").grid(row=0, column=1)
        Button(btn_frame, text="Send Emails",     command=self.send_emails,   width=16,
               font=("times new roman",13,"bold"), bg="red",    fg="white").grid(row=0, column=2)
        Button(btn_frame, text="Reset",           command=self.reset_data,    width=16,
               font=("times new roman",13,"bold"), bg="gray",   fg="white").grid(row=0, column=3)

        # ── Log box for email sending progress ──────────────────
        log_frame = Frame(left_inside_frame, bd=2, relief=RIDGE, bg="white")
        log_frame.place(x=0, y=350, width=715, height=70)

        Label(log_frame, text="Log:", font=("times new roman",11,"bold"), bg="white").pack(anchor=W, padx=5, pady=2)

        self.log_box = Text(log_frame, height=3, width=92, font=("consolas", 9), state=DISABLED,
                            bg="#f8f8f8", fg="#333333", relief=FLAT)
        self.log_box.pack(fill=X, padx=5, pady=0)




        # RIGHT FRAME — same structure as attendance.py right frame
    
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE,
                                 text="Student Attendance Summary",
                                 font=("times new roman", 12, "bold"))
        Right_frame.place(x=750, y=10, width=720, height=580)

        table_frame = Frame(Right_frame, bd=2, relief=RIDGE, bg="white")
        table_frame.place(x=5, y=5, width=710, height=490)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.tbl = ttk.Treeview(table_frame,
            columns=("name","roll","dep","present","total","pct","parent_email","status"),
            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.tbl.xview)
        scroll_y.config(command=self.tbl.yview)

        self.tbl.heading("name",         text="Name")
        self.tbl.heading("roll",         text="Roll")
        self.tbl.heading("dep",          text="Department")
        self.tbl.heading("present",      text="Present")
        self.tbl.heading("total",        text="Total")
        self.tbl.heading("pct",          text="Attendance %")
        self.tbl.heading("parent_email", text="Parent Email")
        self.tbl.heading("status",       text="Email Status")

        self.tbl["show"] = "headings"

        self.tbl.column("name",         width=120)
        self.tbl.column("roll",         width=60)
        self.tbl.column("dep",          width=100)
        self.tbl.column("present",      width=60)
        self.tbl.column("total",        width=50)
        self.tbl.column("pct",          width=85)
        self.tbl.column("parent_email", width=160)
        self.tbl.column("status",       width=90)

        # Same color tags as attendance.py (green=ok, red=low)
        self.tbl.tag_configure("above",    background="#e6f9ec")   
        self.tbl.tag_configure("below",    background="#fde8e8")   
        self.tbl.tag_configure("sent",     background="#e0f0ff")
        self.tbl.tag_configure("failed",   background="#fff3cd")  
        self.tbl.tag_configure("no_email", background="#f5f5f5")  

        self.tbl.pack(fill=BOTH, expand=1)
        self.tbl.bind("<ButtonRelease>", self.get_cursor)

    # ── helpers ────────────────────────────────────────────────
    def _log(self, msg):
        self.log_box.config(state=NORMAL)
        self.log_box.insert(END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_box.see(END)
        self.log_box.config(state=DISABLED)
        self.root.update_idletasks()

    def get_cursor(self, event=""):
        f = self.tbl.focus()
        d = self.tbl.item(f)["values"]
        if not d or len(d) < 7: return
        self.var_name.set(d[0]);  self.var_roll.set(d[1])
        self.var_dep.set(d[2]);   self.var_pct.set(d[5])
        self.var_pemail.set(d[6])

    def load_csv(self):
        fln = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Open Attendance CSV",
            filetypes=(("CSV File","*.csv"),("All File","*.*")), parent=self.root)
        if not fln: return
        self.csv_data.clear()
        with open(fln, newline="", encoding="utf-8-sig") as f:
            for row in csv.reader(f): self.csv_data.append(row)
        self.var_csv_path.set(os.path.basename(fln))
        self._log(f"Loaded {len(self.csv_data)} rows from {os.path.basename(fln)}")
        self._show_all()

    def _get_threshold(self):
        try:    return float(self.var_threshold.get())
        except: return 75.0

    def _calc_all(self):
        threshold = self._get_threshold()
        totals = defaultdict(lambda: {"present":0,"total":0,"roll":"","dep":""})
        for row in self.csv_data:
            if not row: continue
            first = str(row[0]).strip().lower()
            if first in ("attendanceid","id","name",""): continue
            if len(row) >= 7:
                name,roll,dep,status = str(row[1]).strip(),str(row[2]).strip(),str(row[3]).strip(),str(row[6]).strip().lower()
            elif len(row) >= 6:
                name,roll,dep,status = str(row[0]).strip(),str(row[1]).strip(),str(row[2]).strip(),str(row[5]).strip().lower()
            else: continue
            if not name or name.lower() in ("unknown","n/a",""): continue
            totals[name]["total"]  += 1
            totals[name]["roll"]    = roll
            totals[name]["dep"]     = dep
            if status == "present": totals[name]["present"] += 1
        result = []
        for name, v in totals.items():
            pct = round((v["present"]/v["total"]*100), 1) if v["total"] > 0 else 0.0
            result.append({"name":name,"roll":v["roll"],"dep":v["dep"],
                           "present":v["present"],"total":v["total"],
                           "pct":pct,"low":pct < threshold})
        return result, threshold

    def _get_parent_email(self, name, roll):
        try:
            conn = mysql.connector.connect(**DB); cur = conn.cursor()
            cur.execute("SELECT parent_email FROM student WHERE Roll=%s OR Name=%s LIMIT 1",
                        (str(roll), str(name)))
            result = cur.fetchone(); conn.close()
            if result and result[0] and result[0].strip(): return result[0].strip()
        except Exception as e: self._log(f"DB error for {name}: {e}")
        return None

    def _show_all(self):
        if not self.csv_data: return
        all_s, threshold = self._calc_all()
        self.tbl.delete(*self.tbl.get_children())
        low_count = 0
        for s in all_s:
            pe  = self._get_parent_email(s["name"], s["roll"]) or "Not set"
            tag = "below" if s["low"] else "above"
            if s["low"]: low_count += 1
            self.tbl.insert("", END, values=(
                s["name"], s["roll"], s["dep"],
                s["present"], s["total"], f"{s['pct']}%",
                pe, "⚠ Will email" if s["low"] else "✔ OK"
            ), tags=(tag,))
        self._log(f"Showing {len(all_s)} student(s). {low_count} below {threshold}%.")

    def calculate(self):
        if not self.csv_data:
            messagebox.showerror("No Data","Load a CSV file first.",parent=self.root); return
        self._show_all()
        low = [s for s in self._calc_all()[0] if s["low"]]
        threshold = self._get_threshold()
        if not low:
            messagebox.showinfo("All Good",f"All students are at or above {threshold}%.",parent=self.root)
        else:
            messagebox.showinfo("Result",
                f"{len(low)} student(s) below {threshold}%.\n"
                "Click 'Send Emails' to notify parents.",parent=self.root)

    def reset_data(self):
        self.tbl.delete(*self.tbl.get_children())
        self.csv_data.clear()
        self.var_csv_path.set("No file loaded")
        for v in (self.var_name,self.var_roll,self.var_dep,self.var_pct,self.var_pemail): v.set("")
        self.log_box.config(state=NORMAL); self.log_box.delete("1.0",END)
        self.log_box.config(state=DISABLED)

    def send_emails(self):
        sender   = self.var_sender.get().strip()
        password = self.var_password.get().strip()
        college  = self.var_college.get().strip()

        if not sender:
            messagebox.showerror("Config","Enter your Gmail address.",parent=self.root); return
        if not password:
            messagebox.showerror("Config","Enter your Gmail App Password.",parent=self.root); return
        if not self.csv_data:
            messagebox.showerror("No Data","Load a CSV file first.",parent=self.root); return

        all_s, threshold = self._calc_all()
        low = [s for s in all_s if s["low"]]

        if not low:
            messagebox.showinfo("All Good","No students below threshold.",parent=self.root); return
        if not messagebox.askyesno("Confirm",
            f"Send emails to parents of {len(low)} student(s) below {threshold}%?",
            parent=self.root): return

        try:
            self._log("Connecting to Gmail SMTP…")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            self._log("✔ Login successful.")
        except Exception as e:
            self._log(f"✘ Login failed: {e}")
            messagebox.showerror("Login Failed",
                f"Cannot connect to Gmail:\n{e}\n\nUse Gmail App Password.",
                parent=self.root); return

        sent = failed = no_email = 0
        self.tbl.delete(*self.tbl.get_children())

        for s in all_s:
            pe = self._get_parent_email(s["name"], s["roll"])
            if not s["low"]:
                self.tbl.insert("", END, values=(
                    s["name"],s["roll"],s["dep"],
                    s["present"],s["total"],f"{s['pct']}%",
                    pe or "Not set","✔ OK"), tags=("above",))
                continue
            if not pe:
                no_email += 1
                self._log(f"⚠ No parent email for {s['name']}")
                self.tbl.insert("", END, values=(
                    s["name"],s["roll"],s["dep"],
                    s["present"],s["total"],f"{s['pct']}%",
                    "Not set","⚠ No email"), tags=("no_email",)); continue

            subject = f"⚠ Low Attendance Alert — {s['name']} | {college}"
            body = f"""Dear Parent / Guardian,

Your ward's attendance has fallen below the required minimum.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Student Details
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Name         : {s['name']}
  Roll No      : {s['roll']}
  Department   : {s['dep']}

  Attended     : {s['present']} / {s['total']} classes
  Attendance % : {s['pct']}%
  Required     : {threshold}%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Kindly ensure your ward attends classes regularly.

Regards,
{college}
(Automated message — Face Recognition Attendance System)
"""
            try:
                msg = MIMEMultipart()
                msg["From"] = sender; msg["To"] = pe; msg["Subject"] = subject
                msg.attach(MIMEText(body, "plain"))
                server.sendmail(sender, pe, msg.as_string())
                sent += 1
                self._log(f"✔ Sent → {pe}  ({s['name']} — {s['pct']}%)")
                self.tbl.insert("", END, values=(
                    s["name"],s["roll"],s["dep"],
                    s["present"],s["total"],f"{s['pct']}%",
                    pe,"✔ Sent"), tags=("sent",))
            except Exception as e:
                failed += 1
                self._log(f"✘ Failed for {s['name']}: {e}")
                self.tbl.insert("", END, values=(
                    s["name"],s["roll"],s["dep"],
                    s["present"],s["total"],f"{s['pct']}%",
                    pe,"✘ Failed"), tags=("failed",))

        server.quit()
        self._log(f"━━ Done — Sent:{sent}  Failed:{failed}  No email:{no_email} ━━")
        messagebox.showinfo("Email Report",
            f"✔ Sent successfully  : {sent}\n"
            f"✘ Failed             : {failed}\n"
            f"⚠ No parent email    : {no_email}",
            parent=self.root)


if __name__ == "__main__":
    root = Tk()
    obj = EmailSender(root)
    root.mainloop()
