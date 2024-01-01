from db_operations import stu_db_operation as stu_db
import menu_page


class Student:

    column_list = []
    def __init__(self):
        data = stu_db.get_basic_info()
        column_list = stu_db.get_scheme(data["student_tb"])

        for column_name in column_list:
            if column_name != "student_id":
                setattr(self, f"{column_name}", None)

    def personal_details(self):
        for variable in self.__dict__.keys():
            setattr(self, variable, input(f"Enter {variable} : "))




def add_new_student():
    stu1 = Student()
    stu1.personal_details()

    stu_db.insert_student_data(roll_no=stu1.roll_no, first_name=stu1.first_name,
                               last_name=stu1.last_name, age=stu1.age, class_=stu1.class_,
                               father_name=stu1.father_name, address=stu1.address)

def update_student_info():
    id = int(input("Enter student id : "))

    print("What do you want to update ?\n"
          "1. Roll No\n2. First Name\n3. Last Name\n4. Age\n5. Class\n6. Father Name\n7. Address")
    choice = int(input("Enter choice : "))
    column_list = ["roll_no", "first_name", "last_name", "age", "class", "father_name", "address"]

    update_col = column_list[choice - 1]
    stu_db.update_stu_info(id, update_col)

# Main Program

def menu():
    while True:
        print("-----------------------------------------------------------------------------")
        print(f"Press 1 - Add New Student\n"
              f"Press 2 - Check Details of a Student\n"
              f"Press 3 - Delete Details of a Student\n"
              f"Press 4 - Edit Details of a Student\n"
              f"Press 5 - Show all students details\n"
              f"Press b/B - Back to Main Menu\n"
              f"Press q/Q - Exit")

        print("-----------------------------------------------------------------------------")

        ch = input("Enter your choice - ")
        if ch == "1":
            add_new_student()

        if ch == "2":
            id = int(input("Enter student id : "))
            stu_db.get_stu_information(id)

        if ch == "3":
            id = int(input("Enter student id : "))
            stu_db.delete_stu_info(id)

        if ch == "4":
            update_student_info()

        if ch == "5":
            stu_db.stu_all_info()

        if ch in ["b", "B"]:
            menu_page.menu()

        if ch in ["q", "Q"]:
            print("-----------------------------------------------------------------------------")
            print("Thank you!!")
            exit()
