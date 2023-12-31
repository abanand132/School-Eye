import os
from db_operations import stu_db_operation as db
import student_menu
import dept_menu

def menu():
    print("-----------------------------------------------------------------------------")
    print("1. Create New Database\n"
          "2. Department Information\n"
          "3. Student Information\n"
          "c/C. Clear/Clean terminal\n"
          "q/Q. Exit")
    print("-----------------------------------------------------------------------------")

    ch = input("Enter Choice : ")
    if ch == "1":
        print("-----------------------------------------------------------------------------")
        db_name = input("Enter database name : ")
        db.create_db(db_name)

    if ch == "2":
        dept_menu.menu()

    if ch == "3":
        student_menu.menu()

    if ch in ["c", "C"]:
        os.system("cls")
        menu()

    if ch in ["q", "Q"]:
        print("-----------------------------------------------------------------------------")
        print("Thank you!!")
        exit()
