import csv
from os import chdir

class DatabaseHandler:
    def __init__(self, db_path="/home/r0h8n/Desktop/Vanilla/Day4.1/DB"):
        chdir(db_path)

    def get_course(self):
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
        student = {roll_number: {"first_name": first_name, "last_name": last_name, "Total_cost": total_cost,"Enrolled_list": enrolled_list, "Paid": paid}}
        return student

    def make_row_student(self, student):
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
        with open("Student.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["first_name", "last_name", "roll_number", "enrolled_course", "total_course_cost", "total_paid"])
            writer.writerows(self.make_row_student(student))

    def write_courses(self, academy_dict):
        with open("Academy.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Academy", "Courses"])
            for academy, courses in academy_dict.items():
                courses_str = ','.join([f"{course}:{price}" for course, price in courses.items()])
                writer.writerow([academy, courses_str])
    # def add_student(self, student:dict, roll_number):
    #     if int(roll_number) not in student:
    #         student[roll_number] = {}

# Other utility functions can be added as needed
