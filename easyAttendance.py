from tkinter import *
import webbrowser
import subprocess
import os
import sys
from tkinter import messagebox
import socket


def check_server(address, port):
    # Create a TCP socket
    s = socket.socket()
    try:
        s.connect((address, port))
        return True
    except socket.error as e:
        return False

def child(command, directory):
    # Change working directory
    os.chdir(directory)
    # Execute command
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
window.geometry('450x300')
window.resizable(0,0)
def on_closing():
    print("dscsd")
label_image= PhotoImage(file = "design/waterfall.png")
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

btn_image= PhotoImage(file = "design/open.png")
btn = Button(window, text="Open in browser", command=clicked)
btn.config(image=btn_image,width="300",height="150",activebackground="black"
,bg="black", bd=0)
"""
def openclicked():
    if check_server("127.0.0.1",5000):
        webbrowser.open("http://localhost:5000", new=0, autoraise=True)

btn1 = Button(window, text="Open in browser", command=openclicked)
"""
def exit_editor():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        global child
        global started
        """
        try:
            requests.get("http://localhost:5000/clean",timeout=2)
        except Exception as e:
            print(e)
        finally:
            if started:
                child.kill()
            window.destroy()
        """
        if started:
            child.kill()
        window.destroy()

window.protocol('WM_DELETE_WINDOW',exit_editor)
btn.place(x=75,y=95)
#btn1.grid(column=2, row=0)
window.mainloop()
