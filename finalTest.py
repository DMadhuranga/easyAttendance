from tkinter import *
import webbrowser
import subprocess
import os
import sys
from tkinter import messagebox
import socket

def check_server(address, port):
    s = socket.socket()
    try:
        s.connect((address, port))
        return True
    except socket.error as e:
        return False

def child(command, directory):
    os.chdir(directory)
    cmd = subprocess.Popen(command
        , shell=True
        , stdout=subprocess.PIPE
        , stderr=subprocess.PIPE
        , stdin=subprocess.PIPE
    )
    # Retrieve output and error(s), if any
    output = cmd.stdout.read() + cmd.stderr.read()
    # Exiting
    sys.exit(0)

child = 0
started = False
window = Tk()
window.title("Welcome to Easy Attendance")
window.geometry('1000x658')
window.resizable(0,0)
def on_closing():
    print("dscsd")
label_image= PhotoImage(file = "design/background_n.png")
background_label = Label(window, image=label_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
#lbl = Label(window, text="Easy Attendance")
#lbl.grid(column=0, row=0)
def clicked():
    global started
    if not (started or check_server("127.0.0.1",5000)):
        global child
        child = subprocess.Popen(['server.py'], shell=True, creationflags=subprocess.SW_HIDE)
        print(child.pid)
        started = True
    else:
        webbrowser.open("http://localhost:5000", new=0, autoraise=True)

btn_image= PhotoImage(file = "design/Webp.net-resizeimage.png")
btn = Button(window, command=clicked)
btn.config(image=btn_image, width="118",height="118", bd=0)
#btn = Label(window, image=btn_image)
#btn.config(width="120",height="120", bd=0)
#btn.bind('<Button-1>', clicked())
def exit_editor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        global child
        global started
        if started:
            child.kill()
        window.destroy()

window.protocol('WM_DELETE_WINDOW',exit_editor)
btn.place(x=845,y=255)
window.mainloop()
