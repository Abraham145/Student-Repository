import os
from prettytable import PrettyTable
from typing import Iterator, Tuple, IO, List, Dict, DefaultDict
from collections import defaultdict


class Major:
    """
    Stores information about a single student with all of the relevant information
    includes cwid, name, major and container for course grade
    """
    pt_hdr: Tuple[str, str, str] = ["Major", "Required Courses", "Electives"]

    def __init__(self, major: str) -> None:
        """ initializes the variables for the class."""

        self._required: List[str] = list()
        self._electives: List[str] = list()
        self._major: str = major

    def add_course(self, required_elective, course: str) -> None:
        """
        note that this student took course and earned a grade
        """
        if required_elective == 'R':
            self._required.append(course)
        elif required_elective == 'E':
            self._electives.append(course)

    def get_required(self):
        return list(self._required)

    def get_electives(self):
        return list(self._electives)

    def pt_row(self) -> Tuple[str, List[str], List[str]]:
        return self._major, sorted(self._required), sorted(self._electives)


class Student:
    """
    Stores information about a single student with all of the relevant information
    includes cwid, name, major and container for course grade
    """
    pt_hdr: Tuple[str, str, str] = ["CWID", "Name", "Completed Courses", "Remaining Required", "Remaining Electives"]

    def __init__(self, cwid: str, name: str, major: str, required: List[str], electives: List[str]) -> None:
        """ initializes the variables for the class."""
        self._scores: Dict[str, float] = {'A': 4.0, '-A': 3.75, 'B+': 3.25, 'B-': 2.75, 'C+': 2.25, 'C': 2.0, 'C-': 0,
                                          'F': 0.0}
        self._cwid: str = cwid
        self._name: str = name
        self._major: str = major
        self._required_remaining: List[str] = required
        self._electives_remaining: List[str] = electives
        self._courses: Dict[str, str] = {}  # course[course_name] = grade
        self._GPA: Iterator[int] = []

    def add_course(self, course: str, grade: str) -> None:
        """
        note that this student took course and earned a grade
        """
        passing_scores = {'A': 4.0, '-A': 3.75, 'B+': 3.25, 'B-': 2.75, 'C+': 2.25, 'C': 2.0}
        failing_scores = {'C-': 0, 'D': 0, 'F': 0}

        if grade in passing_scores.keys():
            self._courses[course] = grade
            if course in self._required_remaining:
                self._required_remaining.remove(course)
            elif course in self._electives_remaining:
                self._electives_remaining = []
        else:
            pass

    def pt_row(self) -> Tuple[str, str, List[str], List[str], List[str]]:
        return self._cwid, self._name, sorted(self._courses.keys()), self._required_remaining, self._electives_remaining


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
            str, Instructor] = dict()  # key _instructors[cwid] = Student(), value instance of class Student
        self._majors: Dict[str, Major] = dict()
        # self._majors[major] = Major()

        try:
            self._read_majors(path)
            self._read_students(path)
            self._read_instructor(path)
            self._read_grades(path)
        except ValueError as ve:
            print(ve)
        except FileNotFoundError as fnfe:
            print(fnfe)

        if ptables:
            print("\nMajors Summary")
            self.major_table()

            print("\nStudent Summary")
            self.student_table()

            print("\nInstructor Summary")
            self.instructor_table()

    def _read_majors(self, path: str):
        # - use file_reader to read the file one line at a time
        # - read major, R/E, course  # read the line
        for major, required_elective, course in file_reader(os.path.join(path, 'majors.txt'), 3, sep='\t', header=True):
            # - if new major:  # if needed, create a new instance of class Major
            if major not in self._majors:
                # - add new instance of class Major to self._majors[major] = Major(major)
                self._majors[major] = Major(major)

            else:
                # - self._majors[major].add_course(R/E, course)  # add this course to this major
                self._majors[major].add_course(required_elective, course)

    def _read_students(self, path: str) -> None:
        # create new Student(cwid, name, major, required, electives)  # retrieve req, electives from self._majors[major]
        for cwid, name, major in file_reader(os.path.join(path, 'students.txt'), 3, sep=';', header=True):
            self._students[cwid] = Student(cwid, name, major, self._majors[major].get_required(), self._majors[major].get_electives())


    def _read_instructor(self, path: str) -> None:

        for cwid, name, department in file_reader(os.path.join(path, 'instructors.txt'), 3, sep='|', header=True):
            self._instructors[cwid] = Instructor(cwid, name, department)

    def _read_grades(self, path: str) -> None:

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

    def major_table(self) -> None:
        pt: PrettyTable = PrettyTable(field_names=Major.pt_hdr)
        for major in self._majors.values():
            pt.add_row(major.pt_row())
        print(pt)

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
    stevens: Repository = Repository('/Users/Abraham 1/Desktop/SSW810/HW/github-repos/Student-Repository/stevens')


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


main()
