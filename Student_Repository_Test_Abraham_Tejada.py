from typing import Iterator, Tuple
import unittest
from Student_Repository_Abraham_Tejada import Major, Student, Instructor, Repository, file_reader


class RepositoryTest(unittest.TestCase):
    def test_all_tables(self):
        stevens: Repository = Repository('/Users/Abraham 1/Desktop/SSW810/HW/github-repos/Student-Repository/db')

        expect_majors = [
            ('SFEN', "['SSW 555', 'SSW 810']", ['CS 501', 'CS 546'],
             'CS', "['CS 546']", "['SSW 565', 'SSW 810']")]
        expect_students = [
            ('10103','Jobs, S', "['CS 501', 'SSW 810'] ","['SSW 810', 'SSW 555']","['CS 501', 'CS 546']",3.38),
            ('10115', 'Bezos, J', "['SSW 555', 'SSW 810']","['SSW 555']","['CS 501', 'CS 546']",2.0),
            ('10183','Musk, E ',"['CS 546', 'CS 570', 'SSW 810']","[]","['CS 501', 'CS 546']", 4.0),
            ('11714', 'Gates, B', "['CS 546', 'CS 570', 'SSW 810']", "[]", "se()", 3.5)]
        expect_instructors = [
            ('98764','Cohen, R', 'SFEN',' CS 546', 1),
            ('98763','Rowland, J', 'SFEN','SSW 810', 4),
            ('98763', 'Rowland, J', 'SFEN', 'SSW555',1),
            ('98762', 'Hawking, S', 'CS', 'CS 501', 1),
            ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
            ('98762', 'Hawking, S', 'CS', 'CS 570', 1)]
        expect_students_grades = [
            ('Bezos, J', '10115', 'SSW 810', 'A', 'Cohen, R'),
            ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
            ('Bezos, J', '10115', 'CS 546', 'F', 'Cohen, R'),
            ('Bezos, J', '10115', 'CS 546', 'F', 'Rowland, J'),
            ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
            ('Gates, B', '11714', 'CS 546', 'A', 'Hawking, S'),
            ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
            ('Jobs, S', '10103', 'SSW 810', 'A-', 'Cohen, R'),
            ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
            ('Jobs, S', '10103', 'CS 501', 'B', 'Cohen, R'),
            ('Jobs, S', '10103', 'CS 501', 'B', 'Rowland, J'),
            ('Musk, E', '10183', 'SSW 555', 'A', 'Cohen, R'),
            ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
            ('Musk, E', '10183', 'SSW 810', 'A', 'Cohen, R'),
            ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'),
        ]

        students = [student.pt_row() for student in stevens._students.values()]
        majors = [major.pt_row() for major in stevens._students.values()]
        instructors = [row for instructor in stevens._instructors.values() for row in instructor.pt_rows()]
        student_grades = [row for row in stevens.student_db_table('/Users/Abraham 1/Desktop/SSW810/HW/github-repos'
                                                                  '/Student-Repository/db/hw11at.sqlite')]

        self.assertEqual(students, expect_majors)
        self.assertEqual(majors, expect_students)
        self.assertEqual(instructors, expect_instructors)
        self.assertEqual(student_grades, expect_students_grades)


class FileReader(unittest.TestCase):
    def test_file_reader(self):
        expect = [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka', 'Software Engineering'),
                  ('345', 'Benji Cai', 'Software Engineering')]
        result: Iterator[Tuple[str]] = list(file_reader('csv.txt', 3, sep='|', header=True))

        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
