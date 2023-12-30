import db_operation as db
import menu_page


class Student:
    def __init__(self):
        self.roll_no = None
        self.first_name = None
        self.last_name = None
        self.age = None
        self.class_ = None
        self.father_name = None
        self.address = None


    def add_academic_details(self):
        self.class_ = int(input("Enter class in which student read : "))
        self.roll_no = int(input("Roll No. : "))

    def personal_details(self):
        self.first_name = input("First Name : ")
        self.last_name = input("last Name : ")
        self.age = int(input("Age : "))
        self.father_name = input("Father's Name : ")
        self.address = input("Address/City : ")

    # __str__() is used to return the string representation of the object. This function is called when
    # the object of the class is printed.
    def __str__(self):
        return (f"Name : {self.first_name} {self.last_name}\n"
                f"Roll No : {self.roll_no}\nClass : {self.class_}\n"
                f"Age : {self.age}\n"
                f"Father's Name : {self.father_name}\n"
                f"Address : {self.address}")


def add_new_student():
    stu1 = Student()
    stu1.personal_details()
    stu1.add_academic_details()

    db.insert_student_data(roll_no=stu1.roll_no, first_name=stu1.first_name,
                           last_name=stu1.last_name, age=stu1.age, class_=stu1.class_,
                           father_name=stu1.father_name, address=stu1.address)

def update_student_info():
    id = int(input("Enter student id : "))

    print("What do you want to update ?\n"
          "1. Roll No\n2. First Name\n3. Last Name\n4. Age\n5. Class\n6. Father Name\n7. Address")
    choice = int(input("Enter choice : "))
    column_list = ["roll_no", "first_name", "last_name", "age", "class", "father_name", "address"]

    update_col = column_list[choice - 1]
    db.update_stu_info(id, update_col)

# Main Program

def student_func():
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
            db.get_stu_information(id)

        if ch == "3":
            id = int(input("Enter student id : "))
            db.delete_stu_info(id)

        if ch == "4":
            update_student_info()

        if ch == "5":
            db.stu_all_info()

        if ch in ["b", "B"]:
            menu_page.menu()

        if ch in ["q", "Q"]:
            print("-----------------------------------------------------------------------------")
            print("Thank you!!")
            exit()

