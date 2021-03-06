import sqlite3
from sqlite3 import Error
from classes.Student import Student
from classes.Section import Section
import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

class studentDB:

    # studentDB class is the database access class for all the student related information

    def getConnection(db_file):
        # initialize database connection and return database connector

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def createTable(conn):
        # create all the database datatables if they do not exists already

        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS course (course_id integer PRIMARY KEY AUTOINCREMENT,course_code varchar(25) NOT NULL, course_title varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS section (section_id integer PRIMARY KEY AUTOINCREMENT,course_id integer, year YEAR NOT NULL, semester varchar(50) NOT NULL, deleted integer(1) DEFAULT 0, FOREIGN KEY (course_id) REFERENCES course(course_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS session (session_id integer PRIMARY KEY AUTOINCREMENT,section_id integer, date Date NOT NULL, starting_time Time NOT NULL, deleted integer(1) DEFAULT 0,marked integer(1) DEFAULT 0, FOREIGN KEY (section_id) REFERENCES section(section_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS student (id integer PRIMARY KEY AUTOINCREMENT,student_id varchar(25) NOT NULL, student_name varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute("CREATE TABLE IF NOT EXISTS enrollment (id integer,section_id INTEGER, deleted integer(1) DEFAULT 0,PRIMARY KEY(id,section_id), FOREIGN KEY (id) REFERENCES student(id), FOREIGN KEY (section_id) REFERENCES section(section_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS attendance (id integer,session_id INTEGER, attended integer(1) DEFAULT 1,PRIMARY KEY(id,session_id), FOREIGN KEY (id) REFERENCES student(id), FOREIGN KEY (session_id) REFERENCES session(session_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS student_pictures (id integer,image_name VARCHAR(25),deleted integer(1) DEFAULT 0,PRIMARY KEY(id,image_name), FOREIGN KEY (id) REFERENCES student(id))")


    def addStudent(conn,studentId,studentName):
        # create a new entry in student table

        array = [studentId, studentName]
        cursor = conn.cursor()
        cursor.execute("insert into student (student_id,student_name) values (?,?)", array)
        conn.commit()
        return cursor.lastrowid

    def getStudents(conn):
        # get details of all the students (list of student objects)

        if(conn):
            cursor = conn.cursor()
            cursor.execute("select * from student where deleted='0'")
            rows = cursor.fetchall()
            students = []
            for row in rows:
                course = Student(row[0], row[1], row[2])
                students.append(course)
            return students
        return None

    def getStudent(conn,id):
        # get details of a given student (student object)

        if (conn):
            cursor = conn.cursor()
            array = [id]
            cursor.execute("select * from student where id=? and deleted='0'",array)
            rows = cursor.fetchall()
            if(len(rows)==1):
                user = Student(rows[0][0],rows[0][1],rows[0][2])
                return user
        return None

    def getStudentByStudentId(conn,studentId):
        # get details of a student (student object) given the studentId

        if (conn):
            cursor = conn.cursor()
            array = [studentId]
            cursor.execute("select * from student where student_id=? and deleted='0'",array)
            rows = cursor.fetchall()
            if(len(rows)==1):
                user = Student(rows[0][0],rows[0][1],rows[0][2])
                return user
        return None

    def deleteStudent(conn,id):
        # delete a student given the id

        if(conn):
            cursor = conn.cursor()
            array = [id]
            cursor.execute("update student set deleted='1' where id=?", array)
            conn.commit()

    def doesStudentIdExist(conn,studentId):
        # check whether a student exist with the given studentId

        if(conn):
            cursor = conn.cursor()
            array = [studentId]
            cursor.execute("select * from student where student_id=? and deleted='0'", array)
            rows = cursor.fetchall()
            if (len(rows)>0):
                return True
            return False
        return None

    def addSection(conn,id,sectionId):
        # enroll a student to a given section

        if(conn):
            cursor = conn.cursor()
            array = [sectionId, id]
            cursor.execute("insert into enrollment (section_id,id) values (?,?)", array)
            conn.commit()

    def addImage(conn,id,extension):
        # add a new entry ti student_picture table

        if(conn):
            cursor = conn.cursor()
            imageId = str(id)+id_generator()+"."+extension
            array = [id, imageId]
            cursor.execute("insert into student_pictures (id,image_name) values (?,?)", array)
            conn.commit()
            return imageId

    def getSessionPhotos(conn,sessionId):
        # get details of all the photos of students who are registered for the section of given session

        if(conn):
            cursor = conn.cursor()
            array = [sessionId,0]
            cursor.execute("select id,image_name from student_pictures join attendance using(id) where session_id=? and deleted=?", array)
            rows = cursor.fetchall()
            dictionary = {}
            for row in rows:
                if row[0] not in dictionary.keys():
                    dictionary[row[0]] = []
                dictionary[row[0]].append(row[1])
            return dictionary
        return None

    def getEnrolledSections(conn,id):
        # get details of sections (list of section objects) that the given student has registered for

        if(conn):
            cursor = conn.cursor()
            array = [id]
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester from enrollment join section using(section_id) join course using(course_id) where id=?", array)
            sections = []
            rows = cursor.fetchall()
            for row in rows:
                sections.append(Section(row[0], row[1], row[2], row[3], row[4], row[5]))
            return sections
        return None

    def getNumberOfImages(conn,id):
        # get number of images that the given student has registered

        if(conn):
            cursor = conn.cursor()
            array = [id]
            cursor.execute("select * from student_pictures where id=? and deleted='0'", array)
            sections = []
            rows = cursor.fetchall()
            return len(rows)
        return None

    def removeStudentImages(conn,id):
        # remove all the registered images of a student

        if(conn):
            cursor = conn.cursor()
            array = [id]
            cursor.execute("update student_pictures set deleted='1' where id=?", array)
            conn.commit()