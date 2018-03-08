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

tokens = Tokens()
#conn = courseDB.getConnection("database/example.db")
print(courseController.getStudentAttendanceSummaryJSON(2))
#imageController.markAttendance(8)

#studentDB.addStudent(conn,"a001","Mahela Jayawardane")
#courseDB.addCourse(conn,"CS2012","Introduction object oriented programming")
#userDB.addStaff(conn,"staff1","staff1@123")
