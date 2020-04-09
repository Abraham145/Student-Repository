from typing import Iterator, Tuple
import unittest
from Student_Repository_Abraham_Tejada import Majors, Student, Instructor, Repository, file_reader


class RepositoryTest(unittest.TestCase):

    def test_majors_table(self):
        re = Repository('/Users/Abraham 1/Desktop/SSW810/HW/github-repos/Student-Repository/stevens')
        expect = {'10103', 'SSW 567' 'A', '98765'}
        result = re._read_grades('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(result, expect)

    def test_student_table(self):
        re = Repository('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        expect = {'10103', 'Baldwin, C', 'SFEN'}
        result = re._read_students('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(result, expect)

    def test_instructor_table(self):
        re = Repository('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        expect = {'98765', 'Einstein, A', 'SFEN'}
        result = re._read_instructor('/Users/Abraham 1/Desktop/SSW810/HW/lab9/stevens')
        self.assertEqual(result, expect)


class FileReader(unittest.TestCase):
    def test_file_reader(self):
        expect = [('123', 'Jin He', 'Computer Science'), ('234', 'Nanda Koka', 'Software Engineering'),
                  ('345', 'Benji Cai', 'Software Engineering')]
        result: Iterator[Tuple[str]] = list(file_reader('csv.txt', 3, sep='|', header=True))

        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
