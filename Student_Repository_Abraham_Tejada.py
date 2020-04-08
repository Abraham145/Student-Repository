import os
from prettytable import PrettyTable
from typing import Iterator, Tuple, IO, List, Dict, DefaultDict
from collections import defaultdict


class Student:
    """
    Stores information about a single student with all of the relevant information
    includes cwid, name, major and container for course grade
    """
    pt_hdr: Tuple[str, str, str, str, str, str] = ["CWID", "Name", "Completed Courses", "Remaining Required", "Remaining Electives", " GPA"]

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """ initializes the variables for the class."""

        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._courses: Dict[str, str] = {}  # course[course_name] = grade

    def add_course(self, course: str, grade: str) -> None:
        """
        note that this student took course and earned a grade
        """
        self._courses[course]: str = grade

    # create a n
    # def add_remaining_require(self):
    #   read the student file,
    #   extract the remaining course
    #   use set to display
    # def add_remaining_elective(self):
    #     set{}
    # def add_gpa(self):
    #
    #     for grades in 'grades.txt';
    #         gpa =+ grades
    #


    def pt_row(self) -> Tuple[str, str, List[str]]:
        return self._cwid, self._name, sorted(self._courses.keys())


class Instructor:
    """
    Stores information about a single student with all of the relevant information
    includes cwid, name, major and container for course grade
    """
    pt_hdr: List[str] = ["CWID", "Name", "Dept", "Course", "Students"]

    def __init__(self, cwid: str, name: str, department: str) -> None:
        """ initializes the variables for the class."""

        self._cwid: str = cwid
        self._name: str = name
        self._department: str = department
        self._courses: DefaultDict[str, int] = defaultdict(int)  # course[course_name] = number students who taken

    def add_student(self, course: str) -> None:
        """
        note that instructor taught course to one more student
        """
        self._courses[course] += 1

    def pt_rows(self) -> Iterator[Tuple[str, str, str, str, int]]:
        for course, count in self._courses.items():
            yield self._cwid, self._name, self._department, course, count


class Repository:
    """
    holds all of the data for a specific organization
    Includes a container for all students
    Includes a container for all instructors
    """

    def __init__(self, path: str, ptables: bool = True) -> None:
        self._path: str = path
        self._students: Dict[str, Student] = dict()  # key _students[cwid] = Student(), value instance of class Student
        self._instructors: Dict[
            str, Instructor] = dict()  # key _instructors[cwid] = Student(), value instance of class Stu

        try:
            self._read_students(path)
            self._read_instructor(path)
            self._read_grades(path)
            self._read_majors(path)
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)

        if ptables:
            print("\nStudent Summary")
            self.student_table()

            print("\nInstructor Summary")
            self.instructor_table()


    def _read_students(self, path: str) -> None:
        # call file reader - path of the file ( comes from the directory) and the student.txt to
        # the directory os.path.join
        # file reader returns a tuple and you will get cwid, name, major,

        for cwid, name, major in file_reader(os.path.join(path, 'students.txt'), 3, sep=';', header=True):
            self._students[cwid] = Student(cwid, name, major)

    def _read_instructor(self, path: str) -> None:

        for cwid, name, department in file_reader(os.path.join(path, 'instructors.txt'), 3, sep='|', header=True):
            self._instructors[cwid] = Instructor(cwid, name, department)

    def _read_majors(self, path: str) -> None:

        for major, required, electives in file_reader(os.path.join(path, 'majors.txt'), 3, sep='/t', header=True):
            pt: PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Electives'])
            pt.add_row([major, required, electives])
            print(pt)

    def _read_grades(self, path: str) -> None:
        # read student_cwid, course, grade, instructor_cwid
        # tell the student about the course and grade
        # look up student associated with student_cwid, reach inside and update the dictionary inside the student
        # tell the instructor that she taught one more student in the course

        for student_cwid, course, grade, inst_cwid in file_reader(os.path.join(path, 'grades.txt'), 4,
                                                                  sep='|', header=True):
            if student_cwid in self._students:
                self._students[student_cwid].add_course(course, grade)
            else:
                print(f'found grade for unknown student {student_cwid}')

            if inst_cwid in self._instructors:
                self._instructors[inst_cwid].add_student(course)

            else:
                print(f'found grade for unknown instructor {inst_cwid}')


    def student_table(self) -> None:
        pt: PrettyTable = PrettyTable(field_names=Student.pt_hdr)
        for student in self._students.values():
            pt.add_row(student.pt_row())
        print(pt)

    def instructor_table(self) -> None:
        pt: PrettyTable = PrettyTable(field_names=Instructor.pt_hdr)
        for instructor in self._instructors.values():
            for row in instructor.pt_rows():
                pt.add_row(row)
        print(pt)


def main() -> None:
    stevens: Repository = Repository('/Users/Abraham 1/Desktop/SSW810/HW/github-repos/stevens')


def file_reader(path: str, fields: int, sep: str = ',', header: bool = False) -> Iterator[List[str]]:
    """ Write a generator function file_reader() to read field-separated text files and yield a tuple with
    all of the values from a single line in the file on each call to next()
    """
    file_name = path
    try:
        fp: IO = open(file_name, 'r')
    except FileNotFoundError:
        raise FileNotFoundError(f"Can't open {file_name}")
    else:

        with fp:
            for num, line in enumerate(fp, 1):
                tokens: List[str] = line.rstrip('\n').split(sep)
                if fields != len(tokens):
                    raise ValueError(f'{path} has {len(tokens)} fields on {num} but expected {fields}')
                elif num == 1 and header == True:
                    continue
                else:
                    yield tuple(tokens)


check1 = Repository('/Users/Abraham 1/Desktop/SSW810/HW/github-repos/stevens')
