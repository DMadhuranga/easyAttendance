from classes.User import User
from database.userDB import userDB
from classes.Course import Course
from database.courseDB import courseDB
from classes.Student import Student
from database.studentDB import studentDB
from classes.Tokens import Tokens

tokens = Tokens()
conn = courseDB.getConnection("database/example.db")
studentDB.createTable(conn)
#studentDB.addStudent(conn,"a001","Mahela Jayawardane")
#courseDB.addCourse(conn,"CS2012","Introduction object oriented programming")
#userDB.addStaff(conn,"staff1","staff1@123")
print(studentDB.doesStudentIdExist(conn,'a002'))
print("___________________________")
students = studentDB.getStudents(conn)
for student in students:
    student.printStudent()