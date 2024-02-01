# import csv
from check_db import DatabaseHandler
from display_functions import *
import os

class Student:
    def __init__(self, first_name, last_name, roll_number, paid, enrolled=None, total_cost=0, db_handler= DatabaseHandler("/home/r0h8n/Desktop/Vanilla/Day4.1/DB")):
        """
        Initializes a new Student object with the given parameters.

        Args:
            first_name (str): The first name of the student.
            last_name (str): The last name of the student.
            roll_number (int): The roll number of the student.
            paid (float): The amount already paid by the student.
            enrolled (list, optional): List of courses the student is enrolled in. Defaults to an empty list.
            total_cost (float, optional): The total cost for the student. Defaults to 0.
            db_handler (DatabaseHandler, optional): A DatabaseHandler object to interact with the database.
        """
        self.db_handler = db_handler
        self.first_name = first_name
        self.last_name = last_name
        self.roll_number = roll_number
        self.enrolled = enrolled if enrolled is not None else []
        self.paid = paid
        self.total_cost = total_cost
        self.roll_number = int(self.roll_number)

        self.student_data = self.db_handler.get_student()
        if self.roll_number not in self.student_data:
            self.student_data[self.roll_number] = {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "Total_cost": self.total_cost,
                "Enrolled_list": self.enrolled,
                "Paid": self.paid
            }
        else:
            self.student_data[self.roll_number] = {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "Total_cost": self.total_cost,
                "Enrolled_list": self.student_data[self.roll_number]["Enrolled_list"],
                "Paid": self.paid
            }

        self.db_handler.write_student(self.student_data)

    def make_payment(self, pay):
        """
        Processes a payment made by the student.

        Args:
            pay (float): The amount to be paid by the student.
        """
        self.student_data = self.db_handler.get_student()
        self.student_data[self.roll_number]["Paid"] = str(float(self.student_data[self.roll_number]["Paid"]) + pay)
        self.db_handler.write_student(self.student_data)

    def update_total_price(self, id):
        """
        Updates the total cost of courses for the student.

        Args:
            id (int): The roll number of the student.
        """
        self.student_data = self.db_handler.get_student()
        _, all_course_list = self.db_handler.get_course()
        total_cost = 0
        student = self.db_handler.get_student()
        for course in student[id]["Enrolled_list"]:
            if course != "":
                total_cost += int(all_course_list[course])
        self.student_data[id]["Total_cost"] = str(total_cost)
        self.db_handler.write_student(self.student_data)

    def get_remaining_payment(self, id):
        """
        Retrieves the remaining payment amount for the student.

        Args:
            id (int): The roll number of the student.

        Returns:
            float: The remaining amount to be paid by the student.
        """
        self.student_data = DatabaseHandler.get_student(DatabaseHandler)
        student = self.student_data.get(id, "Can't find the id in our Database")
        if isinstance(student, str):
            return student
        remaining = float(student["Total_cost"]) - float(student["Paid"])
        return remaining

    def start_db_handeling(self):
        """
        Initializes database handling for the student.
        """
        self.db_handler = DatabaseHandler()
        
    
    @staticmethod
    def get_student(db_handler):
        """
        Retrieves student data from the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.

        Returns:
            dict: A dictionary containing student data.
        """
        return db_handler.get_student()
    
    @staticmethod
    def write_student(db_handler, student):
        """
        Writes student data to the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
            student (dict): A dictionary containing the student's data.
        """
        return db_handler.write_student(student)

    @classmethod
    def add_student(cls,student:dict):
        """
        Adds a new student to the database.

        Args:
            student (dict): A dictionary containing the new student's data.
        """
        last_roll_number = list(student.keys())[-1]
        full_name = input("\n\nEnter Students full name i.e name and surname only: ").split(" ",1)
        if len(full_name) ==2:
            firstname, lastname = full_name
        else:
            firstname = "".join(full_name)
            lastname = ""
        rollno = input(f"Enter unique rollnumber,(currentlast rollnumber is {last_roll_number}): ")
        current_paid = (input("Enter the current price paid: "))
        if int(rollno)  in student:
            print_colored_message(f"The User with Roll NO {rollno} already exsist. Do you want to edit the user? (y/n):", Colors.RED)
            edit = input()
            if edit.lower() == "y":
                cls(firstname, lastname,rollno,float(current_paid))
            else:
                print_colored_message('''Redirecting back to the Student page......''', Colors.YELLOW)
                 
                cls.add_student(student)  
        else:
            cls(firstname, lastname,rollno,float(current_paid))
        
    
    @classmethod
    def remove_student(cls,db_handler):
        """
        Removes a student from the database based on their roll number.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        try:
            roll_num_to_remove = int(input("Enter the roll number to remove: "))
        except ValueError:
            roll_num_to_remove = int(input("Invalid roll number format, please check roll number and enter again: "))
        student = cls.get_student(db_handler)
        if roll_num_to_remove in student:
            student.pop(int(roll_num_to_remove))
            cls.write_student(db_handler,student)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_remove}", Colors.RED)
        input("\n\nPress anykey to continue...")

    @classmethod
    def show_remaining_fee(cls,db_handler):
        """
        Displays the remaining fee for a specific student.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        student = cls.get_student(db_handler)
        try:
            roll_num_to_fee = int(input("Enter the roll number to get remaning fee: "))
        except ValueError:
            roll_num_to_fee = int(input("Invalid roll number format, please check roll number and enter again: "))
        if roll_num_to_fee in student:
            fee = cls.get_remaining_payment(Student,roll_num_to_fee)
            if fee < 0:
                fee = str(fee *-1) + " Overpaid, please check accounts for refund or enroll to any other course."
            else:
                fee = str(fee) + " Remaning, please pay the fee at time"
            print(fee)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_fee}",Colors.RED)
        input("\n\nPress anykey to continue...")
    
    @classmethod
    def pay_fee(cls,db_handler):
        """
        Processes the fee payment for a specific student.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        student = cls.get_student(db_handler)
        try:
            roll_num_to_pay = int(input("Enter the roll number to get pay fee: "))
        except ValueError:
            roll_num_to_pay = int(input("Invalid roll number format, please check roll number and enter again: "))
        if roll_num_to_pay in student:
            remaining_fee = 'remaning'
            cash_status = "paying"
            fee = cls.get_remaining_payment(cls,roll_num_to_pay)
            refund = False
            if cls.get_remaining_payment(cls,roll_num_to_pay) < 0:
                remaining_fee = "overpaid"
                cash_status = "refunding"
                fee = cls.get_remaining_payment(cls,roll_num_to_pay) * -1
                refund = True

            print(f"The student have {fee} fee {remaining_fee}, {cash_status} the fee now.")
            # student = Student.get_student()
            if not refund:
                student[int(roll_num_to_pay)]["Paid"] = float(student[int(roll_num_to_pay)]["Paid"]) + fee
            else:
                student[int(roll_num_to_pay)]["Paid"] = 0.0
                # refunded = float(student[int(roll_num_to_pay)]['Total_cost'])
                
                # student[int(roll_num_to_pay)]['Total_cost'] = refunded *0.8

            cls.write_student(db_handler,student)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_pay}",Colors.RED)
        input("\n\nEnter anykey to continue....")
    @classmethod
    def join_course(cls, db_handler):
        """
        Enrolls a student in a new course.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        try:
            roll_number_to_join = int(input("Enter the roll number to get Join a course: "))
        except ValueError:
            roll_number_to_join = int(input("Invalid roll number format, please check roll number and enter again: "))
        Academy.show_all_course(db_handler)
        _, all_course_list = Academy.get_course(db_handler)
        course_name_to_add = input("Enter the name of the course you want to add:  ").strip()
        if course_name_to_add in all_course_list:
            student = cls.get_student(db_handler)
            # print(all_course_list)
            if course_name_to_add not in student[roll_number_to_join]["Enrolled_list"]:
                student[roll_number_to_join]["Enrolled_list"].append(course_name_to_add)
                cls.write_student(db_handler,student)
            # s1 = Student()
                cls.update_total_price(cls, roll_number_to_join)
            else:
                print_colored_message(f"The User with roll number {roll_number_to_join} is already enrolled into {course_name_to_add} course",Colors.RED)
        else:
            print_colored_message("No Such Course Name", Colors.RED)
        input("\n Press any key to continue")
    @classmethod
    def opt_course(cls,db_handler):
        """
        Opts a student out of a course.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        try:
            roll_number_to_opt = int(input("Enter the roll number to get Opt from a course: "))
        except ValueError:
            roll_number_to_opt = int(input("Invalid roll number format, please check roll number and enter again: "))
        # show_all_course()
        student = cls.get_student(db_handler)
        course_name_to_remove = input("Enter the name of the course you want to remove:  ")
        if course_name_to_remove in student[roll_number_to_opt]["Enrolled_list"]:
            student[roll_number_to_opt]["Enrolled_list"].remove(course_name_to_remove)
            refunded = float(student[int(roll_number_to_opt)]['Total_cost'])
            paid_total = float(student[int(roll_number_to_opt)]['Paid'])
            student[int(roll_number_to_opt)]['Paid'] = paid_total - (refunded *0.2)
            # print(student)
            # input() 
            cls.write_student(db_handler,student)
            cls.update_total_price(cls,int(roll_number_to_opt))
        else:
            print_colored_message("No Such Course Name", Colors.RED)
            input()
    @classmethod
    def change_session(cls,db_handler):
        """
        Changes the session for all students, checking their fee status.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object.
        """
        print_colored_message("\n\t\tChanging Session",Colors.GREEN)
        student = Student.get_student(db_handler)
        for key, values in student.items():
            remaning = Student.get_remaining_payment(Student, int(key))
            if  remaning > 0:
                print_colored_message(f"\t\tThe Student {values['first_name']} have {remaning} fee, please check whith him/her once",Colors.RED)
            if  remaning < 0:
                remaning = remaning * -1
                print_colored_message(f"\t\tThe Student {values['first_name']} {values['last_name']} have {remaning} fee over charged, please check whith him/her once",Colors.GREEN)
        input("\n\nContinue ....")

class Academy:

    def start_db_handeling(self):
        """
        Initializes database handling for the academy.
        """
        self.db_handler = DatabaseHandler()
        
    @staticmethod  
    def add_academy(all_academy,db_handler):
        """
        Adds a new academy and its courses to the database.

        Args:
            all_academy (dict): A dictionary containing all academies and their courses.
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.
        """
        # all_academy, _ =  db_handler.get_course()
        academy_name = input("Enter Name of Academy: ")
        course_detail = input("Enter Academy details like (Coursename:price,coursename2:price) :")
        courses = course_detail.split(",")
        for course in courses:
            courses_name, course_price = course.split(":")
            if academy_name not in all_academy:
                all_academy[academy_name] = {courses_name:course_price}
            else:
                all_academy[academy_name].update({courses_name:course_price})
        db_handler.write_courses(all_academy)
        

    @staticmethod
    def remove_academy(all_academy,db_handler):
        """
        Removes an academy from the database.

        Args:
            all_academy (dict): A dictionary containing all academies and their courses.
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.
        """
        remove = input("Enter Academy Name: ")
        if remove in all_academy:
            all_academy.pop(remove)
            db_handler.write_courses(all_academy)
        else:
            print_colored_message(f"Cant find the Academy named {remove}",Colors.RED)
        input("\n\nContinue...")
    
    @staticmethod
    def show_all_course(db_handler):
        """
        Displays all courses and their details from the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.
        """
        os.system("clear")
        _, all_course_list = db_handler.get_course()
        print('''Course Name \t\t\t\t\t\t\t Course Price''')
        print("_"*100)
        for key, value in all_course_list.items():
            key = key.strip()
            if len(key) < 50:
                key += " " * (50-len(key))
            print_colored_message(f"{key} \t:\t {value.strip()}", Colors.YELLOW)
        input("\n\nContinue...")

    @staticmethod
    def get_course(db_handler):
        """
        Retrieves all courses from the database.

        Args:
            db_handler (DatabaseHandler): A DatabaseHandler object to interact with the database.

        Returns:
            tuple: A tuple containing a dictionary of all courses and their details.
        """
        return db_handler.get_course()

    
