from classes.User import User
from database.userDB import userDB
from classes.Course import Course
from database.courseDB import courseDB
from classes.Student import Student
from database.studentDB import studentDB
from classes.Tokens import Tokens
from classes.Recognizer import Recognizer
import cv2
import random
import string
from controllers.courseController import courseController

#imageController.saveVideo(7,360)
#tokens = Tokens()
#conn = courseDB.getConnection("database/example.db")
#print(courseController.getStudentAttendanceSummaryJSON(2))
#imageController.markAttendance(8)

#studentDB.addStudent(conn,"a001","Mahela Jayawardane")
#courseDB.addCourse(conn,"CS2012","Introduction object oriented programming")
#userDB.addStaff(conn,"staff1","staff1@123")


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
window.geometry('350x200')
def on_closing():
    print("dscsd")
lbl = Label(window, text="Hello")
lbl.grid(column=0, row=0)
def clicked():
    global started
    if not (started or check_server("127.0.0.1",5000)):
        global child
        child = subprocess.Popen(['server.py'], shell=True, creationflags=subprocess.SW_HIDE)
        print(child.pid)
        started = True
    else:
        webbrowser.open("http://localhost:5000", new=0, autoraise=True)

btn = Button(window, text="Start Server", command=clicked)
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
btn.grid(column=1, row=0)
#btn1.grid(column=2, row=0)
window.mainloop()
