
import db_operation as db
import stu_info
import os

def menu():
    print("-----------------------------------------------------------------------------")
    print("1. Create New Database\n"
          "2. Create new student table\n"
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
        db.create_stu_details_tb()

    if ch == "3":
        stu_info.student_func()

    if ch in ["c", "C"]:
        os.system("cls")
        menu()

    if ch in ["q", "Q"]:
        print("-----------------------------------------------------------------------------")
        print("Thank you!!")
        exit()
