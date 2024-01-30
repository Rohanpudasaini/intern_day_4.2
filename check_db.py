import csv
from os import chdir

class DatabaseHandler:
    def __init__(self, db_path="/home/r0h8n/Desktop/Vanilla/Day4.1/DB"):
        """
        Initializes a new DatabaseHandler object with the given database path.

        Args:
            db_path (str, optional): The file path to the database. Defaults to "/home/r0h8n/Desktop/Vanilla/Day4.1/DB".
        """
        chdir(db_path)

    def get_course(self):
        """
        Retrieves all courses and their details from the 'Academy.csv' file.

        Returns:
            tuple: A tuple containing two dictionaries, one with academies as keys and courses as values, and another with all courses and their prices.
        """
        academy_dict = {}
        all_academy = {}
        with open("Academy.csv", "r") as file:
            reader = csv.reader(file)
            for i, rows in enumerate(reader):
                if i == 0:
                    continue
                academy, courses = rows
                courses = courses.split(',')
                for course in courses:
                    course_name, course_price = course.split(":")
                    course_name = course_name.strip()
                    if academy not in academy_dict:
                        academy_dict[academy] = {course_name: course_price}
                    else:
                        academy_dict[academy].update({course_name: course_price})
                    if course_name not in all_academy:
                        all_academy[course_name] = course_price
                    else:
                        new_course_name = (f"{course_name} - {academy}")
                        all_academy[new_course_name] = course_price
        return academy_dict, all_academy

    def get_student(self):
        """
        Retrieves all student data from the 'Student.csv' file.

        Returns:
            dict: A dictionary containing student data with roll numbers as keys.
        """
        student = {}
        with open("Student.csv", 'r') as file:
            reader = csv.reader(file)
            for i, rows in enumerate(reader):
                if i == 0:
                    continue
                first_name, last_name, roll_number, enrolled, total_cost, paid = rows
                roll_number = int(roll_number)
                enrolled_list = enrolled.split(",")
                
                student[roll_number] = {"first_name": first_name.strip(), "last_name": last_name.strip(),
                                    "Total_cost": total_cost.strip(), "Enrolled_list": enrolled_list, "Paid": paid.strip()}
        return student

    def create_student(self, first_name, last_name, roll_number, paid, enrolled_list=[], total_cost=0):
        """
        Creates a new student entry.

        Args:
            first_name (str): The first name of the student.
            last_name (str): The last name of the student.
            roll_number (int): The roll number of the student.
            paid (float): The amount already paid by the student.
            enrolled_list (list, optional): List of courses the student is enrolled in. Defaults to an empty list.
            total_cost (float, optional): The total cost for the student. Defaults to 0.

        Returns:
            dict: A dictionary representing the new student.
        """
        student = {roll_number: {"first_name": first_name, "last_name": last_name, "Total_cost": total_cost,"Enrolled_list": enrolled_list, "Paid": paid}}
        return student

    def make_row_student(self, student):
        """
        Formats student data into rows suitable for CSV writing.

        Args:
            student (dict): A dictionary containing the student's data.

        Returns:
            list: A list of lists, each representing a row of student data.
        """
        rows = []
        for roll_number, details in student.items():
            first_name = details['first_name']
            last_name = details['last_name']
            total_cost = details['Total_cost']
            paid = details['Paid']
            enrolled = ','.join(details['Enrolled_list'])
            row = [first_name, last_name, str(roll_number), enrolled, total_cost, paid]
            rows.append(row)
        return rows

    def write_student(self, student):
        """
        Writes student data to the 'Student.csv' file.

        Args:
            student (dict): A dictionary containing the student's data.
        """
        with open("Student.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "roll_number", "enrolled_course", "total_course_cost", "total_paid"])
            writer.writerows(self.make_row_student(student))

    def write_courses(self, academy_dict):
        """
        Writes course data to the 'Academy.csv' file.

        Args:
            academy_dict (dict): A dictionary containing academies and their associated courses.
        """
        with open("Academy.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Academy", "Courses"])
            for academy, courses in academy_dict.items():
                courses_str = ','.join([f"{course}:{price}" for course, price in courses.items()])
                writer.writerow([academy, courses_str])

