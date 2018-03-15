import unittest
from database.studentDB import studentDB
from classes.Student import Student
from classes.Section import Section
import sqlite3


class GetConnectionTestCase(unittest.TestCase):
    def test_with_valid_db_details(self):
        self.assertIsInstance(studentDB.getConnection('../database/example.db'),sqlite3.Connection)

    def test_with_invalid_db_details(self):
        self.assertEqual(studentDB.getConnection('/database/example.db'),None,"Incorect, database connect details are wrong")

class getStudentsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_users(self):
        self.assertIsInstance(studentDB.getStudents(self.conn)[0],Student)

    def test_for_set(self):
        self.assertIsInstance(studentDB.getStudents(self.conn), list)

    def test_for_invalid_connection(self):
        self.assertEqual(studentDB.getStudents(False), None,"Incorrect, connection is closed")

class getStudentTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_Student(self):
        self.assertIsInstance(studentDB.getStudent(self.conn,'1'),Student)

    def test_for_invalid_student(self):
        self.assertEqual(studentDB.getStudent(self.conn,"0"), None,"Incorrect, id is not valid")

class getStudentByStudentIdTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_studentname(self):
        self.assertIsInstance(studentDB.getStudentByStudentId(self.conn,'a000'),Student)

    def test_for_invalid_studentname(self):
        self.assertEqual(studentDB.getStudentByStudentId(self.conn,"a12sd"), None,"Incorrect, student id is not valid")

class doesStudentIdExistTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_existing_student_id(self):
        self.assertEqual(studentDB.doesStudentIdExist(self.conn,'a000'),True,"Incorrect, student id exist")

    def test_for_non_existing_student_id(self):
        self.assertEqual(studentDB.doesStudentIdExist(self.conn,"a12sd"), False,"Incorrect, student id does not exist")

class getSessionPhotosTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_student_dictionary(self):
        self.assertIsInstance(studentDB.getSessionPhotos(self.conn,'12'),dict)

    def test_for_photos(self):
        photoSet = studentDB.getSessionPhotos(self.conn,'12')
        self.assertIsInstance(photoSet[list(photoSet.keys())[0]], list)

    def test_for_non_existing_session(self):
        self.assertEqual(len(studentDB.getSessionPhotos(self.conn,'6').keys()),0, "Incorrect, there should be no students")

class getEnrolledSectionsTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_student(self):
        self.assertIsInstance(studentDB.getEnrolledSections(self.conn,'6'),list)

    def test_for_valid_student_sections(self):
        self.assertIsInstance(studentDB.getEnrolledSections(self.conn,'6')[0],Section)

    def test_for_non_existing_student(self):
        self.assertEqual(len(studentDB.getEnrolledSections(self.conn,'0')),0, "Incorrect, there should be no sections")

class getNumberOfImagesTestCase(unittest.TestCase):
    def setUp(self):
        self.dbName = '../database/example.db'
        self.conn = studentDB.getConnection(self.dbName)

    def tearDown(self):
        self.conn.close()

    def test_for_valid_student(self):
        self.assertEqual(studentDB.getNumberOfImages(self.conn, '1')>0, True, "Incorrect, there should be photos")

    def test_for_non_existing_student(self):
        self.assertEqual(studentDB.getNumberOfImages(self.conn,'0'),0, "Incorrect, there should be no photos")