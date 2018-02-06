import sqlite3
from sqlite3 import Error
from classes.Student import Student

class studentDB:
    def getConnection(db_file):
        try:
            conn = sqlite3.connect(db_file)
            return conn
        except Error as e:
            print(e)
        return None

    def createTable(conn):
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS course (course_id integer PRIMARY KEY AUTOINCREMENT,course_code varchar(25) NOT NULL, course_title varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS section (section_id integer PRIMARY KEY AUTOINCREMENT,course_id integer, year YEAR NOT NULL, semester varchar(50) NOT NULL, deleted integer(1) DEFAULT 0, FOREIGN KEY (course_id) REFERENCES course(course_id))")
        cursor.execute("CREATE TABLE IF NOT EXISTS student (id integer PRIMARY KEY AUTOINCREMENT,student_id varchar(25) NOT NULL, student_name varchar(200) NOT NULL, deleted integer(1) DEFAULT 0)")
        cursor.execute("CREATE TABLE IF NOT EXISTS enrollment (id integer,section_id INTEGER, deleted integer(1) DEFAULT 0,PRIMARY KEY(id,section_id), FOREIGN KEY (id) REFERENCES student(id), FOREIGN KEY (section_id) REFERENCES section(section_id))")


    def addStudent(conn,studentId,studentName):
        array = [studentId, studentName]
        cursor = conn.cursor()
        cursor.execute("insert into student (student_id,student_name) values (?,?)", array)
        conn.commit()
        return cursor.lastrowid

    def getStudents(conn):
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
        if(conn):
            cursor = conn.cursor()
            array = [id]
            cursor.execute("update student set deleted='1' where id=?", array)
            conn.commit()

    def doesStudentIdExist(conn,studentId):
        if(conn):
            cursor = conn.cursor()
            array = [studentId]
            cursor.execute("select * from student where student_id=? and deleted='0'", array)
            rows = cursor.fetchall()
            if (len(rows)>0):
                return True
            return False
        return None