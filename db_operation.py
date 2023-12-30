import mysql.connector
# from mysql.connector.errors import Error
import json
import menu_page
import stu_info


def get_basic_info():
    with open('basic_info.json', 'r') as info:
        data = json.load(info)
    return data

def make_connection(data):
    mydb = mysql.connector.connect(
        host="localhost",
        user=data["db_user"],
        password=data["db_password"],
        database=data["database"]
    )
    return mydb


def create_db(database_name: str):
    """
    It'll create a database in the mysql
    :param database_name: Name of the database
    :return: None
    """
    # establishing connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="System-abhishek"
    )

    cursor = mydb.cursor()

    db_query = f'''CREATE DATABASE IF NOT EXISTS {database_name}'''
    cursor.execute(db_query)

    # updating name of student table
    with open("basic_info.json", 'r') as info:
        data = json.load(info)
    data["database"] = database_name
    with open('basic_info.json', 'w') as info:
        json.dump(data, info, indent=4)

    print(f"Database named '{database_name}' created successfully...")

    # closing the connections
    cursor.close()
    mydb.close()
    menu_page.menu()

def create_stu_details_tb(table_name: str = "student_info"):
    """
    It will create a table which contains student's information
    :param table_name: (string) Enter table name
    :return: None
    """
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    # writing sql query
    create_tb_query = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                          student_id INT PRIMARY KEY AUTO_INCREMENT,
                          roll_no INT NOT NULL,
                          first_name VARCHAR(20),
                          last_name VARCHAR(20),
                          age INT,
                          class INT,
                          father_name VARCHAR(50),
                          address VARCHAR(60)
                          )'''

    # executing sql query
    cursor.execute(create_tb_query)

    # updating name of student table
    with open("basic_info.json", 'r') as info:
        data = json.load(info)
    data["student_tb"] = table_name
    with open('basic_info.json', 'w') as info:
        json.dump(data, info, indent=4)

    print(f"Table '{table_name}' created successfully...")

    # closing the connections
    cursor.close()
    mydb.close()
    menu_page.menu()


def insert_student_data(roll_no: int, first_name: str, last_name: str, age: int,
                        class_: int, father_name: str, address: str):
    """ It helps in inserting data of the student in the database
    :param roll_no: roll no. of the student
    :param first_name: first name of the student
    :param last_name: middle + last name of the student
    :param age: age of the student
    :param class_: class in which the student is studying
    :param father_name: father's name of the student
    :param address: present address of the student
    :return:
    """
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    insert_query = f'''INSERT INTO {data["student_tb"]} 
                       (roll_no, first_name, last_name, age, class, father_name, address)
                       VALUES 
                       (%s, %s, %s, %s, %s, %s, %s) '''

    column_val = (roll_no, first_name, last_name, age, class_, father_name, address)

    cursor.execute(insert_query, column_val)
    mydb.commit()
    print("-------------------------- OUTPUT -------------------------------------------")
    print(cursor.rowcount, "rows affected...")

    cursor.execute(f'''SELECT COUNT(student_id) FROM {data["student_tb"]}''')
    result = cursor.fetchall()
    print(f"Student id of {first_name} : {result[0][0]}")

    # closing the connections
    cursor.close()
    mydb.close()
    stu_info.student_func()


def get_stu_information(id):
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    query = f'''SELECT * FROM {data["student_tb"]}
                WHERE student_id = {id}'''

    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) > 0:
        for x in result:
            print(x)
    else:
        print("No records found...")

    # closing the connections
    cursor.close()
    mydb.close()
    stu_info.student_func()

def delete_stu_info(id):
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    query = f'''DELETE FROM {data["student_tb"]}
                WHERE student_id = {id} '''

    cursor.execute(query)
    mydb.commit()
    print("-------------------------- OUTPUT -------------------------------------------")
    print(cursor.rowcount, " rows affected.")

    # closing the connections
    cursor.close()
    mydb.close()
    stu_info.student_func()

def update_stu_info(id, update_col):
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    cursor.execute(f'''SELECT * FROM {data["student_tb"]}
                       WHERE student_id = {id}''')
    result = cursor.fetchall()
    if len(result) == 0:
        print("-----------------------------------------------------------------------------")
        print("No records found...")
    else:
        current_info = result[0]
        print("-----------------------------------------------------------------------------")
        print(f"Current details :\n{current_info}")
        print(f"\nDo you want to update '{update_col}' column ? Press 'y' for yes / 'n' for no ?")
        ch = input("Enter choice : ")
        if ch == "y" and update_col not in ["roll_no", "class", "age"]:
            new_data = input("Enter new data : ")
            query = f'''UPDATE {data["student_tb"]}
                        SET {update_col} = {new_data}
                        WHERE student_id = {id}'''
            cursor.execute(query)
            mydb.commit()
            print("-------------------------- OUTPUT -------------------------------------------")
            print(cursor.rowcount, "row affected")

        elif ch == "y":
            new_data = int(input("Enter new data : "))
            query = f'''UPDATE {data["student_tb"]}
                                SET {update_col} = {new_data}
                                WHERE student_id = {id}'''
            cursor.execute(query)
            mydb.commit()
            print("-------------------------- OUTPUT -------------------------------------------")
            print(cursor.rowcount, "row affected")

        else:
            print("-------------------------- OUTPUT -------------------------------------------")
            print("No data updated!!")
            stu_info.student_func()


    # closing the connections
    cursor.close()
    mydb.close()
    stu_info.student_func()

def stu_all_info():
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    query = f'''SELECT * FROM {data["student_tb"]}'''
    cursor.execute(query)
    data = cursor.fetchall()

    print("-------------------------- OUTPUT -------------------------------------------")
    print(f"{len(data)} records found...")
    print("student id, roll no, first_name, last_name, age, class, father_name, address")
    for stu_data in data:
        print("-----------------------------------------------------------------------------")
        print(stu_data)

    # closing the connections
    cursor.close()
    mydb.close()
    stu_info.student_func()
