import db_operations.stu_db_operation as stu_db
import menu_page


def student_tb_menu():
    print("-----------------------------------------------------------------------------")
    print("1. Create new student table\n"
          "2. Modify student table\n"
          "b/B. Back to Dept. Menu\n"
          "q/Q. Exit")
    ch = input("\nEnter choice : ")
    if ch == "1":
        tb_name = input("Enter table name : ")
        stu_db.create_stu_details_tb(tb_name)

    if ch == "2":
        stu_db.modify_stu_tb_schema()

    if ch in ["b", "B"]:
        menu()

    if ch in ["q", "Q", "quit"]:
        print("---------------------- EXIT -------------------------------------------------")
        print("Thank you!!!")
        exit()
def menu():
    print("---------------------- DEPARTMENT MENU ------------------------------------------")
    print("1. Student Table\n"
          "2. Teacher Table\n"
          "3. Fees Table\n"
          "b/B. Back to Main Menu\n"
          "q/Q. Exit")
    ch = input("\nEnter choice : ")

    if ch == "1":
        student_tb_menu()

    if ch == "2":
        pass

    if ch == "3":
        pass

    if ch == 4:
        pass

    if ch in ["b", "B"]:
        menu_page.menu()

    if ch in ["q", "Q", "quit"]:
        print("-----------------------------------------------------------------------------")
        print("Thank you!!!")
        exit()
