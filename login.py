from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

DB = dict(host="localhost", user="root", password="root123", database="face_recognition")
DEFAULT_USER = "parthpaliwal"
DEFAULT_PASS = "1458"


class Login:
    def __init__(self, root):
        self.root = root
        self.root.geometry("480x560+500+150")
        self.root.title("Face Recognition System — Login")
        self.root.resizable(False, False)
        self.root.configure(bg="white")
        self.success = False

        # ── Title bar ──────────────────────────────────────────
        title_lbl = Label(self.root, text="FACE RECOGNITION SYSTEM",
                          font=("Times New Roman", 18, "bold"),
                          bg="#0f4c81", fg="white", bd=4, relief=RIDGE)
        title_lbl.place(x=0, y=0, width=480, height=50)

        # ── Sub title ─────────────────────────────────────────
        Label(self.root, text="Attendance Management — Login",
              font=("times new roman", 12), bg="#1a6fbd", fg="white"
              ).place(x=0, y=50, width=480, height=28)

        # ── Logo area ─────────────────────────────────────────
        logo_frame = Frame(self.root, bg="#f0f4ff", bd=2, relief=RIDGE)
        logo_frame.place(x=150, y=95, width=180, height=100)

        # Draw simple face icon on canvas
        ic = Canvas(logo_frame, width=100, height=80,
                    bg="#f0f4ff", highlightthickness=0)
        ic.place(x=40, y=10)
        ic.create_oval(10,5,90,70, outline="#0f4c81", width=3, fill="#dce8ff")
        ic.create_oval(25,22,42,38, fill="#0f4c81", outline="")
        ic.create_oval(58,22,75,38, fill="#0f4c81", outline="")
        ic.create_line(15,48,85,48, fill="#0f4c81", width=1, dash=(4,3))
        ic.create_arc(26,46,74,66, start=200, extent=140,
                      outline="#0f4c81", width=2, style=ARC)

        # ── Login card ─────────────────────────────────────────
        card = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        card.place(x=40, y=210, width=400, height=300)

        Label(card, text="🔐  Sign In to Continue",
              font=("times new roman", 14, "bold"),
              bg="#0f4c81", fg="white"
              ).place(x=0, y=0, width=400, height=38)

        # Username
        Label(card, text="Username:", font=("times new roman",12,"bold"),
              bg="white").place(x=20, y=58)
        self.var_user = StringVar()
        user_entry = ttk.Entry(card, textvariable=self.var_user,
                               width=28, font=("times new roman",12))
        user_entry.place(x=20, y=82)
        user_entry.focus()

        # Password
        Label(card, text="Password:", font=("times new roman",12,"bold"),
              bg="white").place(x=20, y=118)
        self.var_pass = StringVar()
        self.pass_entry = ttk.Entry(card, textvariable=self.var_pass,
                                    width=28, font=("times new roman",12), show="*")
        self.pass_entry.place(x=20, y=142)

        # Show password
        self.show_var = BooleanVar(value=False)
        def toggle_show():
            self.pass_entry.config(show="" if self.show_var.get() else "*")
        Checkbutton(card, text="Show Password",
                    variable=self.show_var, command=toggle_show,
                    font=("times new roman",11), bg="white", cursor="hand2"
                    ).place(x=20, y=174)

        # Error label
        self.err_var = StringVar(value="")
        Label(card, textvariable=self.err_var,
              font=("times new roman",10), bg="white", fg="red"
              ).place(x=20, y=205, width=360)

        # Login button
        Button(card, text="LOGIN",
               command=self.do_login,
               font=("times new roman",14,"bold"),
               bg="#0f4c81", fg="white",
               cursor="hand2", relief=FLAT
               ).place(x=20, y=232, width=360, height=44)

        self.root.bind("<Return>", lambda e: self.do_login())

        # ── Footer ─────────────────────────────────────────────
        Label(self.root, text=f"Default:  {DEFAULT_USER}  /  {DEFAULT_PASS}",
              font=("times new roman",9), bg="white", fg="gray"
              ).place(x=0, y=520, width=480)

        Label(self.root, text="© Face Recognition Attendance System",
              font=("times new roman",9), bg="white", fg="gray"
              ).place(x=0, y=540, width=480)

    def do_login(self):
        username = self.var_user.get().strip()
        password = self.var_pass.get().strip()

        if not username or not password:
            self.err_var.set("⚠  Username and password are required.")
            return

        authenticated = False
        # Try DB login table first
        try:
            conn = mysql.connector.connect(**DB)
            cur  = conn.cursor()
            cur.execute("""SELECT COUNT(*) FROM information_schema.TABLES
                           WHERE TABLE_SCHEMA='face_recognition'
                           AND TABLE_NAME='admin_login'""")
            if cur.fetchone()[0] > 0:
                cur.execute(
                    "SELECT * FROM admin_login WHERE username=%s AND password=%s",
                    (username, password))
                if cur.fetchone():
                    authenticated = True
            conn.close()
        except Exception:
            pass

        # Fallback: default credentials
        if not authenticated:
            if username == DEFAULT_USER and password == DEFAULT_PASS:
                authenticated = True

        if authenticated:
            self.err_var.set("")
            self.success = True
            self.root.destroy()
        else:
            self.err_var.set("✘  Invalid username or password. Try again.")
            self.var_pass.set("")
            self.pass_entry.focus()


def run_login():
    root = Tk()
    app  = Login(root)
    root.mainloop()
    return app.success


if __name__ == "__main__":
    if run_login():
        from main import Face_Recognition_System
        root = Tk()
        Face_Recognition_System(root)
        root.mainloop()
