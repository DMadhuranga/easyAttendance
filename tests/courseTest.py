import unittest
from database.courseDB import courseDB
from classes.Student import Student
from classes.Section import Section
from classes.Course import Course
from classes.Session import Session
from classes.Attendance import Attendance
import sqlite3

class GetConnectionTestCase(unittest.TestCase):
    def test_with_valid_db_details(self):
        self.assertIsInstance(courseDB.getConnection('../database/example.db'),sqlite3.Connection)

    def test_with_invalid_db_details(self):
        self.assertEqual(courseDB.getConnection('/database/example.db'),None,"Incorect, database connect details are wrong")

class getCoursesTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_courses(self):
        self.assertIsInstance(courseDB.getCourses(self.conn)[0],Course)

    def test_for_set(self):
        self.assertIsInstance(courseDB.getCourses(self.conn), list)

    def test_for_invalid_connection(self):
        self.assertEqual(courseDB.getCourses(False), None,"Incorrect, connection is closed")

class getCourseTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_course(self):
        self.assertIsInstance(courseDB.getCourse(self.conn,'1'),Course)

    def test_for_invalid_course(self):
        self.assertEqual(courseDB.getCourse(self.conn,"0"), None,"Incorrect, course id is not valid")

class getCourseByCodeTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_coursecode(self):
        self.assertIsInstance(courseDB.getCourseByCode(self.conn,'CS1245'),Course)

    def test_for_invalid_coursecode(self):
        self.assertEqual(courseDB.getCourseByCode(self.conn,"CS1115"), None,"Incorrect, course code is not valid")

class getSectionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_course(self):
        self.assertIsInstance(courseDB.getSections(self.conn,'1')[0],Section)

    def test_for_invalid_course(self):
        self.assertEqual(len(courseDB.getSections(self.conn,"0")), 0,"Incorrect, course is not valid")

class getSectionTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_course(self):
        self.assertIsInstance(courseDB.getSection(self.conn,'1'),Section)

    def test_for_invalid_course(self):
        self.assertEqual(courseDB.getSection(self.conn,"0"), None,"Incorrect, section is not valid")

class getSessionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_section(self):
        self.assertIsInstance(courseDB.getSessions(self.conn,'2'),list)

    def test_for_valid_section_sessions(self):
        self.assertIsInstance(courseDB.getSessions(self.conn,'2')[0],Session)

    def test_for_non_existing_section(self):
        self.assertEqual(len(courseDB.getSessions(self.conn,'0')),0, "Incorrect, there should be no sessions")

class getSessionTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_session(self):
        self.assertIsInstance(courseDB.getSession(self.conn,'12'),Session)

    def test_for_invalid_session(self):
        self.assertEqual(courseDB.getSession(self.conn,"0"), None,"Incorrect, session id is not valid")

class getAllSessionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_sessions(self):
        self.assertIsInstance(courseDB.getAllSessions(self.conn)[0],Session)

    def test_for_set(self):
        self.assertIsInstance(courseDB.getAllSessions(self.conn), list)

    def test_for_invalid_connection(self):
        self.assertEqual(courseDB.getAllSessions(False), None,"Incorrect, connection is closed")

class getAttendanceTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_sessions(self):
        self.assertIsInstance(courseDB.getAttendance(self.conn,"12")[0],Attendance)

    def test_for_set(self):
        self.assertIsInstance(courseDB.getAttendance(self.conn,"12"), list)

    def test_for_invalid_session(self):
        self.assertEqual(len(courseDB.getAttendance(self.conn,"0")), 0,"Incorrect, session id is not valid")

class getSectionStudentsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_students(self):
        self.assertIsInstance(courseDB.getSectionStudents(self.conn,"2")[0],Student)

    def test_for_set(self):
        self.assertIsInstance(courseDB.getSectionStudents(self.conn,"2"), list)

    def test_for_invalid_session(self):
        self.assertEqual(len(courseDB.getSectionStudents(self.conn,"0")), 0,"Incorrect, section id is not valid")

class getNotSectionStudentsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_students(self):
        self.assertIsInstance(courseDB.getNotSectionStudents(self.conn,"2")[0],Student)

    def test_for_set(self):
        self.assertIsInstance(courseDB.getNotSectionStudents(self.conn,"2"), list)

class getSectionAttendanceSummaryTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_students(self):
        sessions = courseDB.getSectionAttendanceSummary(self.conn,"2")
        self.assertIsInstance(sessions[list(sessions.keys())[0]]["students"],list)

    def test_for_dictionary(self):
        self.assertIsInstance(courseDB.getSectionAttendanceSummary(self.conn,"2"), dict)

class getUnmarkedSessionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = courseDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_sessions(self):
        self.assertIsInstance(courseDB.getUnmarkedSessions(self.conn)[0],Session)

    def test_for_set(self):
        self.assertIsInstance(courseDB.getUnmarkedSessions(self.conn), list)