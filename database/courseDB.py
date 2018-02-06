import sqlite3
from sqlite3 import Error
from classes.Course import Course
from classes.Section import Section
from classes.Session import Session

class courseDB:
    def getConnection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def createTable(conn):
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS course (course_id integer PRIMARY KEY AUTOINCREMENT,course_code varchar(25) NOT NULL, course_title varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute("CREATE TABLE IF NOT EXISTS section (section_id integer PRIMARY KEY AUTOINCREMENT,course_id integer, year YEAR NOT NULL, semester varchar(50) NOT NULL, deleted integer(1) DEFAULT 0, FOREIGN KEY (course_id) REFERENCES course(course_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS session (session_id integer PRIMARY KEY AUTOINCREMENT,section_id integer, date Date NOT NULL, starting_time Time NOT NULL, deleted integer(1) DEFAULT 0, FOREIGN KEY (section_id) REFERENCES section(section_id))")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS student (id integer PRIMARY KEY AUTOINCREMENT,student_id varchar(25) NOT NULL, student_name varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS enrollment (id integer,section_id INTEGER, deleted integer(1) DEFAULT 0,PRIMARY KEY(id,section_id), FOREIGN KEY (id) REFERENCES student(id), FOREIGN KEY (section_id) REFERENCES section(section_id))")

    def addCourse(conn,courseCode,courseTitle):
        array = [courseCode, courseTitle]
        cursor = conn.cursor()
        cursor.execute("insert into course (course_code,course_title) values (?,?)", array)
        conn.commit()
        return cursor.lastrowid

    def getCourses(conn):
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
        if(conn):
            cursor = conn.cursor()
            array = [courseId]
            cursor.execute("update course set deleted='1' where course_id=?", array)
            conn.commit()

    def addSection(conn,courseId,year,semester):
        if(conn):
            cursor = conn.cursor()
            array = [courseId,year,semester]
            cursor.execute("insert into section (course_id,year,semester) values (?,?,?)",array)
            conn.commit()
            return cursor.lastrowid
        return None

    def addStudent(conn,sectionId,id):
        if(conn):
            cursor = conn.cursor()
            array = [sectionId, id]
            cursor.execute("insert into enrollment (section_id,id) values (?,?)", array)
            conn.commit()

    def getSections(conn,courseId):
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
        if(conn):
            cursor = conn.cursor()
            array = [sectionId,date,time]
            cursor.execute("insert into session (section_id,date,starting_time) values (?,?,?)",array)
            conn.commit()
            return cursor.lastrowid
        return None

    def getSessions(conn,sectionId):
        if (conn):
            cursor = conn.cursor()
            array = [sectionId]
            cursor.execute("select course_id,course_code,course_title,section_id,year,semester,session_id,date,starting_time from (section join course using(course_id)) join session using(section_id) where section_id = ?", array)
            sessions = []
            rows = cursor.fetchall()
            for row in rows:
                session = Session(row[0], row[1], row[2],row[3], row[4],row[5],row[6], row[7],row[8])
                sessions.append(session)
            return sessions
        return None