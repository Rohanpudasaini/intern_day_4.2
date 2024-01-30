import os
from check_db import DatabaseHandler
from cli_app_class import Student, Academy
from display_functions import *

def show_student_rows(db_handler):
    os.system("clear")
    student = Student.get_student(db_handler)
    print("Student Name |\t| Student Roll Number |\t| Enrolled List")
    for key, values in student.items():
        name = f"{values['first_name']} {values['last_name']}"
        count = len(name)
        if count < 15:
            name += " "*(15-count)
        if "" in values['Enrolled_list']:
            values['Enrolled_list'].remove('')
        print_colored_message(f"{name} |\t| {key} |\t\t| {values['Enrolled_list']}",Colors.YELLOW)
    choice = show_student_menu()
    match choice:
        case "1":
            Student.add_student(student)
            show_student_rows(db_handler)

        case "2":
            Student.remove_student(db_handler)
            show_student_rows(db_handler)

        case "3":
            Student.show_remaining_fee(db_handler)
            show_student_rows(db_handler)

        case "4":
            Student.pay_fee(db_handler)
            show_student_rows(db_handler)
            
        case "5":
            Student.join_course(db_handler)
            show_student_rows(db_handler)

        case "6":
            Student.opt_course(db_handler)
            show_student_rows(db_handler)

        case "7":
            Student.change_session(db_handler)
            show_student_rows(db_handler)
        
        case "8":
            show_main_menu()
        case _:
            show_student_rows(db_handler)

def show_university(db_handler):
    os.system("clear")
    all_academy, _ = Academy.get_course(db_handler)
    print('''Academy Name \t\t\t\t\t\t Courses and Price''')
    for key, values in all_academy.items():
        print("_"*80)
        print_colored_message(f"{key}", Colors.YELLOW)
        print("_"*80)
        for key2, values2 in values.items():
            print_colored_message(f"\t\t\t {key2.strip()}: {values2}",Colors.YELLOW) 
    choice = show_courses_menu()
    match choice:
        case "1":
            Academy.add_academy(all_academy,db_handler)
        case "2":
            Academy.remove_academy(all_academy, db_handler)
        case "3":
            show_main_menu()
        case _:
            show_university(db_handler)

def main():
    show_welcome_screen()
    db_handler = DatabaseHandler()
    Student.start_db_handeling(Student)
    Academy.start_db_handeling(Academy)
    while True:
        choice = show_main_menu()
        if choice == '1':
            show_student_rows(db_handler)
        elif choice == '2':
            show_university(db_handler)
        elif choice == '3':
            Academy.show_all_course(db_handler)
        elif choice == '4':
            print("Exiting the app...")
            exit()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
