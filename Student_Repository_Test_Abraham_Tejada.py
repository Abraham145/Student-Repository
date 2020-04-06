from typing import Iterator, Tuple
import unittest
from HW09_Abraham_Tejada import Student, Instructor, Repository, file_reader


class TestStudent(unittest.TestCase):

    def test_init_(self):
        s: Student = Student('123', 'robert', 'eng')
        self.assertEqual(s._cwid, '123')
        self.assertEqual(s._name, 'robert')
        self.assertEqual(s._major, 'eng')


class InstructorTest(unittest.TestCase):
    def test_init_(self):
        i: Instructor = Instructor('123', 'chris', 'eng')
        self.assertEqual(i._cwid, '123')
        self.assertEqual(i._name, 'chris')
        self.assertEqual(i._department, 'eng')


class RepositoryTest(unittest.TestCase):
    def test_init_(self):
        r: Repository = Repository('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(r._path, '/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')

    def test_read_student(self):
        re = Repository('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        expect = {'10103', 'Baldwin, C', 'SFEN'}
        result = re._read_students('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(result, expect)

    def test_read_instructor(self):
        re = Repository('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        expect = {'98765', 'Einstein, A', 'SFEN'}
        result = re._read_instructor('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(result, expect)

    def test_read_grades(self):
        re = Repository('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        expect = {'10103', 'SSW 567' 'A', '98765'}
        result = re._read_grades('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(result, expect)


#
class FileReader(unittest.TestCase):
    def test_file_reader(self):
        expect = [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka', 'Software Engineering'),
                  ('345', 'Benji Cai', 'Software Engineering')]
        result: Iterator[Tuple[str]] = list(file_reader('csv.txt', 3, sep='|', header=True))

        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
