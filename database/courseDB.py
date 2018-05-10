import sqlite3
import datetime
from sqlite3 import Error
from classes.Course import Course
from classes.Section import Section
from classes.Session import Session
from classes.Attendance import Attendance
from classes.Student import Student
from classes.SessionAttendance import SessionAttendance

class courseDB:

    #courseDB class is the database access class for all the course related information

    def getConnection(db_file):
        #initialize database connection and return database connector

        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def createTable(conn):
        #create all the database datatables if they do not exists already

        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS course (course_id integer PRIMARY KEY AUTOINCREMENT,course_code varchar(25) NOT NULL, course_title varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute("CREATE TABLE IF NOT EXISTS section (section_id integer PRIMARY KEY AUTOINCREMENT,course_id integer, year YEAR NOT NULL, semester varchar(50) NOT NULL, deleted integer(1) DEFAULT 0, FOREIGN KEY (course_id) REFERENCES course(course_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS session (session_id integer PRIMARY KEY AUTOINCREMENT,section_id integer, date Date NOT NULL, starting_time Time NOT NULL, deleted integer(1) DEFAULT 0,marked integer(1) DEFAULT 0, FOREIGN KEY (section_id) REFERENCES section(section_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS student (id integer PRIMARY KEY AUTOINCREMENT,student_id varchar(25) NOT NULL, student_name varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS enrollment (id integer,section_id INTEGER, deleted integer(1) DEFAULT 0,PRIMARY KEY(id,section_id), FOREIGN KEY (id) REFERENCES student(id), FOREIGN KEY (section_id) REFERENCES section(section_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS attendance (id integer,session_id INTEGER, attended integer(1) DEFAULT 0,PRIMARY KEY(id,session_id), FOREIGN KEY (id) REFERENCES student(id), FOREIGN KEY (session_id) REFERENCES session(session_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS student_pictures (id integer,image_name VARCHAR(25),deleted integer(1) default 0,PRIMARY KEY(id,image_name), FOREIGN KEY (id) REFERENCES student(id))")

    def addCourse(conn,courseCode,courseTitle):
        # adding a new course to the course table given the course code and course title

        array = [courseCode, courseTitle]
        cursor = conn.cursor()
        cursor.execute("insert into course (course_code,course_title) values (?,?)", array)
        conn.commit()
        return cursor.lastrowid

    def getCourses(conn):
        # return details of all courses (list of course objects)

        if(conn):
            cursor = conn.cursor()
            cursor.execute("select * from course where deleted='0'")
            rows = cursor.fetchall()
            courses = []
            for row in rows:
                course = Course(row[0], row[1], row[2])
                courses.append(course)
            return courses
        return None

    def getCourse(conn,courseId):
        # return details of a course (course object) given the courseId

        if (conn):
            cursor = conn.cursor()
            array = [courseId]
            cursor.execute("select * from course where course_id=? and deleted='0'",array)
            rows = cursor.fetchall()
            if(len(rows)==1):
                user = Course(rows[0][0],rows[0][1],rows[0][2])
                return user
        return None

    def getCourseByCode(conn,courseCode):
        # return details of a course (course object) given the course code

        if (conn):
            cursor = conn.cursor()
            array = [courseCode]
            cursor.execute("select * from course where course_code=? and deleted='0'",array)
            rows = cursor.fetchall()
            if(len(rows)==1):
                user = Course(rows[0][0],rows[0][1],rows[0][2])
                return user
        return None

    def deleteCourse(conn,courseId):
        # delete a course from course table given the courseId

        if(conn):
            cursor = conn.cursor()
            array = [courseId]
            cursor.execute("update course set deleted='1' where course_id=?", array)
            conn.commit()

    def addSection(conn,courseId,year,semester):
        # add a section to the section table given the year, semester and courseId of the course that section belong to

        if(conn):
            cursor = conn.cursor()
            array = [courseId,year,semester]
            cursor.execute("insert into section (course_id,year,semester) values (?,?,?)",array)
            conn.commit()
            return cursor.lastrowid
        return None

    def addStudent(conn,sectionId,id):
        # add a student to a given section

        if(conn):
            cursor = conn.cursor()
            array = [sectionId, id]
            cursor.execute("insert into enrollment (section_id,id) values (?,?)", array)
            conn.commit()

    def getSections(conn,courseId):
        # return details of all sections (list of section objects)

        if (conn):
            cursor = conn.cursor()
            array = [courseId]
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester from section join course using(course_id) where course_id = ?", array)
            sections = []
            rows = cursor.fetchall()
            for row in rows:
                section = Section(row[0], row[1], row[2],row[3], row[4],row[5])
                sections.append(section)
            return sections
        return None

    def getSection(conn,secionId):
        # return details of a section (section object) given the sectionId

        if (conn):
            cursor = conn.cursor()
            array = [secionId]
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester from section join course using(course_id) where section_id = ?", array)
            sections = []
            rows = cursor.fetchall()
            if(len(rows)==1):
                row = rows[0]
                return Section(row[0], row[1], row[2],row[3], row[4],row[5])
        return None

    def addSession(conn,sectionId,date,time):
        # add a session to the session database table given the data, time and the sectionId of the section that session belongs to

        if(conn):
            cursor = conn.cursor()
            array = [sectionId,date,time]
            cursor.execute("select id from enrollment where section_id=?",[sectionId])
            rows = cursor.fetchall()
            cursor.execute("insert into session (section_id,date,starting_time) values (?,?,?)",array)
            sessionId = cursor.lastrowid
            sql = "insert into attendance (session_id,id) values "
            data = []
            for row in rows:
                sql = sql +"(?,?),"
                data.append(sessionId)
                data.append(row[0])
            sql = sql[0:-1]
            if(len(data)>0):
                cursor.execute(sql,data)
            conn.commit()
            return sessionId
        return None

    def getSessions(conn,sectionId):
        # get details of all the sessions (list of session objects) of a given section

        if (conn):
            cursor = conn.cursor()
            array = [sectionId]
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester,session_id,date,starting_time,marked from (section join course using(course_id)) join session using(section_id) where section_id = ?", array)
            sessions = []
            rows = cursor.fetchall()
            for row in rows:
                session = Session(row[0], row[1], row[2],row[3], row[4],row[5],row[6], row[7],row[8],row[9])
                sessions.append(session)
            return sessions
        return None

    def getSession(conn,sessionId):
        # get details of a session (session object) given the sessionId

        if (conn):
            cursor = conn.cursor()
            array = [sessionId]
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester,session_id,date,starting_time,marked from (section join course using(course_id)) join session using(section_id) where session_id = ?", array)
            sections = []
            rows = cursor.fetchall()
            if(len(rows)==1):
                row = rows[0]
                return Session(row[0], row[1], row[2],row[3], row[4],row[5],row[6],row[7],row[8],row[9])
        return None

    def getAllSessions(conn):
        # get details of all the sessions (list of session objects)

        if (conn):
            cursor = conn.cursor()
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester,session_id,date,starting_time,marked from (section join course using(course_id)) join session using(section_id) ORDER BY date")
            sessions = []
            rows = cursor.fetchall()
            for row in rows:
                session = Session(row[0], row[1], row[2],row[3], row[4],row[5],row[6], row[7],row[8],row[9])
                sessions.append(session)
            return sessions
        return None

    def getAttendance(conn,sessionId):
        # get attendance details of all the student (list of attendance objects) in a given session

        if (conn):
            cursor = conn.cursor()
            array = [sessionId]
            cursor.execute("select id,student_id,student_name,session_id,attended from attendance join student using(id) where session_id = ?", array)
            attendances = []
            rows = cursor.fetchall()
            for row in rows:
                attendance = Attendance(row[0], row[1], row[2],row[3], row[4])
                attendances.append(attendance)
            return attendances
        return None

    def markAttendance(conn,sessionId,id):
        # mark attendance as present of a given student in a given session

        if(conn):
            cursor = conn.cursor()
            array = [sessionId,id]
            cursor.execute("update attendance set attended='1' where session_id=? and id=?)",array)
            conn.commit()
            return True
        return None

    def getSectionStudents(conn,sectionId):
        # get details of all the students (list of section objects) in a given section

        if (conn):
            cursor = conn.cursor()
            array = [sectionId]
            cursor.execute("select id,student_id,student_name from enrollment join student using(id) where section_id = ?", array)
            students = []
            rows = cursor.fetchall()
            for row in rows:
                student = Student(row[0], row[1], row[2])
                students.append(student)
            return students
        return None

    def markAttendanceToDB(conn,sessionId,ids):
        # mark attendance as present of a set of given students in a given session

        if (conn):
            cursor = conn.cursor()
            for id in ids:
                array = [sessionId, id]
                cursor.execute("update attendance set attended='1' where session_id=? and id=?", array)
                conn.commit()
            cursor.execute("update session set marked='1' where session_id=?", [sessionId])
            conn.commit()
            return True
        return None

    def getNotSectionStudents(conn,sectionId):
        # get the details of students (list of student objects) that are not registered for a given section

        if (conn):
            cursor = conn.cursor()
            array = [sectionId]
            cursor.execute("select id,student_id,student_name from student where id NOT IN (select id from enrollment where section_id = ?)", array)
            students = []
            rows = cursor.fetchall()
            for row in rows:
                student = Student(row[0], row[1], row[2])
                students.append(student)
            return students
        return None

    def enrollStudent(conn,sectionId,id):
        # enroll (create a new entry in enrollment table) the given student to given section

        if(conn):
            cursor = conn.cursor()
            array = [sectionId,id]
            cursor.execute("insert into enrollment (section_id,id) values (?,?)",array)
            conn.commit()
            return True
        return None

    def getSectionAttendanceSummary(conn,sectionId):
        # get the attendance of each session (no of present, no of all students) in the given section

        if (conn):
            cursor = conn.cursor()
            array = [sectionId]
            cursor.execute("select section_id,session_id,date,starting_time,marked,id,student_id,student_name,attended from (session join attendance using(session_id)) join student using(id) where session.section_id=? order by session.date, session.session_id", array)
            sessions = {}
            ret_sessions = {}
            rows = cursor.fetchall()
            for row in rows:
                if not row[1] in sessions:
                    sessions[row[1]] = SessionAttendance(row[0],row[1],row[2],row[3],row[4])
                sessions[row[1]].addStudent(row[5],row[6],row[7],row[8])

                if not row[1] in ret_sessions:
                    ret_sessions[row[1]] = {"sectionId":row[0],"sessionId":row[1],"date":row[2],"startingTime":row[3],"marked":row[4],"students":[]}
                ret_sessions[row[1]]["students"].append([row[5],row[6],row[7],row[8]])
            return ret_sessions
        return None

    def getUnmarkedSessions(conn):
        # get details of all the unmarked sessions (list of session objects)

        if (conn):
            cursor = conn.cursor()
            todate = datetime.datetime.today().strftime('%Y-%m-%d')
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester,session_id,date,starting_time,marked from (section join course using(course_id)) join session using(section_id) where session.marked='0' and session.date='"+todate+"' ORDER BY date")
            sessions = []
            rows = cursor.fetchall()
            for row in rows:
                session = Session(row[0], row[1], row[2],row[3], row[4],row[5],row[6], row[7],row[8],row[9])
                sessions.append(session)
            return sessions
        return None

    def getTodayAttendanceSummary(conn):
        # get details of marked and unmarked sessions of today
        if (conn):
            todate = datetime.datetime.today().strftime('%Y-%m-%d')
            cursor = conn.cursor()
            array = [todate]
            cursor.execute("select session_id,marked,id,attended from session join attendance using(session_id) where session.date=? order by session.session_id", array)
            sessions = []
            noOfMarkedSessions = 0
            noOfUnMarkedSessions = 0
            noOfAttendedStudents = 0
            noOfAbsentStudents = 0
            rows = cursor.fetchall()
            totalStudents = len(rows)
            for row in rows:
                if not row[0] in sessions:
                    sessions.append(row[0])
                    if row[1]==0:
                        noOfUnMarkedSessions+=1
                    else:
                        noOfMarkedSessions+=1
                if (row[1]==1) and (row[3]==0):
                    noOfAbsentStudents+=1
                elif (row[1]==1) and (row[3]==1):
                    noOfAttendedStudents+=1
            return {"noOfMarkedSessions":noOfMarkedSessions,"noOfUnMarkedSessions":noOfUnMarkedSessions,"totalStudents":totalStudents,"noOfAttendedStudents":noOfAttendedStudents,"noOfAbsentStudents":noOfAbsentStudents}
        return None