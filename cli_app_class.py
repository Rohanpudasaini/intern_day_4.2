# import csv
from check_db import DatabaseHandler
from display_functions import *
import os

class Student:
    def __init__(self, first_name, last_name, roll_number, paid, enrolled=None, total_cost=0, db_handler= DatabaseHandler("/home/r0h8n/Desktop/Vanilla/Day4.1/DB")):
        self.db_handler = db_handler
        self.first_name = first_name
        self.last_name = last_name
        self.roll_number = roll_number
        self.enrolled = enrolled if enrolled is not None else []
        self.paid = paid
        self.total_cost = total_cost
        self.roll_number = int(self.roll_number)

        self.student_data = self.db_handler.get_student()
        # print(self.student_data)
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
        # print(self.student_data)
        # input("Testing")
        self.db_handler.write_student(self.student_data)

    def make_payment(self, pay):
        # self.start_db_handeling(self)
        self.student_data = self.db_handler.get_student()
        self.student_data[self.roll_number]["Paid"] = str(float(self.student_data[self.roll_number]["Paid"]) + pay)
        self.db_handler.write_student(self.student_data)

    def update_total_price(self, id):
        # self.start_db_handeling(self)
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
        # self.start_db_handeling(self)
        self.student_data = DatabaseHandler.get_student(DatabaseHandler)
        student = self.student_data.get(id, "Can't find the id in our Database")
        if isinstance(student, str):
            return student
        remaining = float(student["Total_cost"]) - float(student["Paid"])
        return remaining
    # def remaining_payment(self, id) ->float:
    #     self.student = self.db_handler.get_student()
    #     self.student = self.student.get(id, "Can't find the id in our Database")
    #     remaning = float(self.student["Total_cost"])- float(self.student["Paid"])
    #     return remaning

    def start_db_handeling(self):
        self.db_handler = DatabaseHandler()
        
    
    @staticmethod
    def get_student(db_handler):
        return db_handler.get_student()
    
    @staticmethod
    def write_student(db_handler, student):
        return db_handler.write_student(student)

    
    def add_student(self,student:dict):
        last_roll_number = list(student.keys())[-1]
        full_name = input("Enter Students full name i.e name and surname only: ").split(" ",1)
        if len(full_name) ==2:
            firstname, lastname = full_name
        else:
            firstname = "".join(full_name)
            lastname = ""
        rollno = input(f"Enter unique rollnumber,(currentlast rollnumber is {last_roll_number}): ")
        current_paid = (input("Enter the current price paid: "))
        self(firstname, lastname,rollno,float(current_paid))
    
    
    def remove_student(self,db_handler):
        roll_num_to_remove = int(input("Enter the roll number to remove: "))
        student = self.get_student(db_handler)
        if roll_num_to_remove in student:
            student.pop(int(roll_num_to_remove))
            self.write_student(db_handler,student)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_remove}", Colors.RED)
        input("\n\nPress anykey to continue...")

    def show_remaining_fee(self,db_handler):
        student = self.get_student(db_handler)
        roll_num_to_fee = int(input("Enter the roll number to get remaning fee "))
        if roll_num_to_fee in student:
            fee = self.get_remaining_payment(Student,roll_num_to_fee)
            if fee < 0:
                fee = str(fee *-1) + " Overpaid"
            else:
                fee = str(fee) + " Remaning"
            print(fee)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_fee}",Colors.RED)
        input("\n\nPress anykey to continue...")
    
    def pay_fee(self,db_handler):
        student = self.get_student(db_handler)
        roll_num_to_pay = int(input("Enter the roll number to get pay fee: "))
        if roll_num_to_pay in student:
            remaining_fee = 'remaning'
            cash_status = "paying"
            fee = self.get_remaining_payment(self,roll_num_to_pay)
            if self.get_remaining_payment(self,roll_num_to_pay) < 0:
                remaining_fee = "overpaid"
                cash_status = "refunding"
                fee = self.get_remaining_payment(self,roll_num_to_pay) * -1
                refund = True

            print(f"The student have {fee} fee {remaining_fee}, {cash_status} the fee now.")
            # student = Student.get_student()
            if not refund:
                student[int(roll_num_to_pay)]["Paid"] = float(student[int(roll_num_to_pay)]["Paid"]) + fee
            else:
                student[int(roll_num_to_pay)]["Paid"] = 0.0
            self.write_student(db_handler,student)
        else:
            print_colored_message(f"No student with roll number {roll_num_to_pay}",Colors.RED)
        input("\n\nEnter anykey to continue....")

    def join_course(self, db_handler):
        roll_number_to_join = int(input("Enter the roll number to get Join a course: "))
        Academy.show_all_course(db_handler)
        _, all_course_list = Academy.get_course(db_handler)
        course_name_to_add = input("Enter the name of the course you want to add:  ").strip()
        if course_name_to_add in all_course_list:
            student = self.get_student(db_handler)
            # print(all_course_list)
            if course_name_to_add not in student[roll_number_to_join]["Enrolled_list"]:
                student[roll_number_to_join]["Enrolled_list"].append(course_name_to_add)
                self.write_student(db_handler,student)
            # s1 = Student()
                self.update_total_price(self, roll_number_to_join)
            else:
                print_colored_message(f"The User with roll number {roll_number_to_join} is already enrolled into {course_name_to_add} course",Colors.RED)
        else:
            print_colored_message("No Such Course Name", Colors.RED)
        input("\n Press any key to continue")
    
    def opt_course(self,db_handler):
        roll_number_to_opt = int(input("Enter the roll number to get Opt from a course: "))
        # show_all_course()
        student = self.get_student(db_handler)
        course_name_to_remove = input("Enter the name of the course you want to remove:  ")
        if course_name_to_remove in student[roll_number_to_opt]["Enrolled_list"]:
            student[roll_number_to_opt]["Enrolled_list"].remove(course_name_to_remove)
            self.write_student(db_handler,student)
            self.update_total_price(self,int(roll_number_to_opt))
        else:
            print_colored_message("No Such Course Name", Colors.RED)
            input()
    
    def change_session(self,db_handler):
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
        self.db_handler = DatabaseHandler()
        
    @staticmethod  
    def add_academy(all_academy,db_handler):
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
        remove = input("Enter Academy Name: ")
        if remove in all_academy:
            all_academy.pop(remove)
            db_handler.write_courses(all_academy)
        else:
            print_colored_message(f"Cant find the Academy named {remove}",Colors.RED)
        input("\n\nContinue...")
    
    @staticmethod
    def show_all_course(db_handler):
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
        return db_handler.get_course()

    
