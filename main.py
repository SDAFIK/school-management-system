# School Management System (File Handling + OOP + Encapsulation)

import os

DATA_FILE = "students.txt"

class Course:
    def __init__(self, name: str):
        self.name = name.strip()

    def __str__(self):
        return self.name


class Student:
    def __init__(self, name: str, roll: str, courses=None, password: str = ""):
        self.name = name.strip()
        self.roll = roll.strip()
        self.courses = courses if courses is not None else []
        self.__password = password  # Private variable (Encapsulation)

    # Getter method (Encapsulation demo)
    def get_password(self):
        return self.__password

    # Optional: password update method
    def set_password(self, new_password: str):
        self.__password = new_password

    def add_course(self, course: Course):
        self.courses.append(course)

    def courses_as_string(self):
        return ",".join([c.name for c in self.courses])

    @staticmethod
    def from_line(line: str):
        """
        File format per line:
        roll|name|course1,course2,course3|password
        """
        parts = line.strip().split("|")
        if len(parts) < 4:
            return None

        roll, name, course_str, password = parts[0], parts[1], parts[2], parts[3]
        courses = []
        if course_str.strip():
            for c in course_str.split(","):
                courses.append(Course(c))
        return Student(name=name, roll=roll, courses=courses, password=password)

    def to_line(self):
    
        return f"{self.roll}|{self.name}|{self.courses_as_string()}|{self.get_password()}\n"


class SchoolManager:
    def __init__(self, filename: str):
        self.filename = filename
        # Ensure file exists
        if not os.path.exists(self.filename):
            with open(self.filename, "w", encoding="utf-8") as f:
                pass

    def enroll_student(self, student: Student):
        """
        New student save to file (append mode)
        """
        # roll duplicate check
        if self.find_student_by_roll(student.roll) is not None:
            print("⚠️ Roll already exists! Enrollment failed.")
            return

        with open(self.filename, "a", encoding="utf-8") as f:
            f.write(student.to_line())
        print("✅ Student enrolled & saved successfully!")

    def show_all_students(self):
        """
        Read file and print all students
        """
        print("\n All Students List:")
        print("-" * 60)

        has_data = False
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                student = Student.from_line(line)
                if student:
                    has_data = True
                    print(f"Roll: {student.roll}")
                    print(f"Name: {student.name}")
                    print(f"Courses: {student.courses_as_string() if student.courses else 'None'}")
                    # password show only via getter (Encapsulation demo)
                    print(f"Password (via getter): {student.get_password()}")
                    print("-" * 60)

        if not has_data:
            print("❌ No students found (file is empty).")
            print("-" * 60)

    def find_student_by_roll(self, roll: str):
        """
        Search student by roll from file
        """
        roll = roll.strip()
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                student = Student.from_line(line)
                if student and student.roll == roll:
                    return student
        return None


def menu():
    print("\n # welcome to School Management System #  ")
    print("1. Enroll New Student")
    print("2. Show All Students")
    print("3. Search Student by Roll")
    print("4. Exit")
    return input("Choose an option (1-4): ").strip()


def main():
    manager = SchoolManager(DATA_FILE)

    while True:
        choice = menu()

        if choice == "1":
            name = input("Enter student name: ").strip()
            roll = input("Enter student roll: ").strip()
            password = input("Set a password (hidden info): ").strip()

            course_input = input("Enter courses (comma separated, e.g., Math,English): ").strip()
            courses = []
            if course_input:
                for c in course_input.split(","):
                    courses.append(Course(c))

            student = Student(name=name, roll=roll, courses=courses, password=password)
            manager.enroll_student(student)

        elif choice == "2":
            manager.show_all_students()

        elif choice == "3":
            roll = input("Enter roll to search: ").strip()
            student = manager.find_student_by_roll(roll)
            if student:
                print("\n✅ Student Found!")
                print(f"Roll: {student.roll}")
                print(f"Name: {student.name}")
                print(f"Courses: {student.courses_as_string() if student.courses else 'None'}")
                print(f"Password (via getter): {student.get_password()}")
            else:
                print("❌ No student found with this roll.")

        elif choice == "4":
            print(" Exiting... Data is saved in students.txt")
            break

        else:
            print("⚠️ Invalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()
