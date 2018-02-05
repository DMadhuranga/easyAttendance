import sqlite3
from sqlite3 import Error
from classes.Course import Course

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