import mysql.connector
import json
import menu_page
import student_menu
import dept_menu

def get_basic_info():
    with open("db_operations/database_info.json", 'r') as info:
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
    with open("db_operations/database_info.json", 'r') as info:
        data = json.load(info)
    data["database"] = database_name
    with open('db_operations/database_info.json', 'w') as info:
        json.dump(data, info, indent=4)

    print(f"Database named '{database_name}' created successfully...")

    # closing the connections
    cursor.close()
    mydb.close()
    menu_page.menu()

def get_scheme(tb_name):
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    query = f'''DESC {tb_name}'''
    cursor.execute(query)
    result = cursor.fetchall()
    column_list = []
    for column in result:
        column_list.append(column[0])

    return column_list

def create_stu_details_tb(table_name: str):
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
                          class_ INT,
                          father_name VARCHAR(50),
                          address VARCHAR(60)
                          )'''

    # executing sql query
    cursor.execute(create_tb_query)

    # updating name of student table
    with open("db_operations/database_info.json", 'r') as info:
        data = json.load(info)
    data["student_tb"] = table_name
    with open('db_operations/database_info.json', 'w') as info:
        json.dump(data, info, indent=4)

    print(f"Table '{table_name}' created successfully...")
    print("Current schema of the table - ")
    print("-----------------------------------------------------------------------------")
    scheme = get_scheme(f"{table_name}")
    print(scheme)

    # closing the connections
    cursor.close()
    mydb.close()
    dept_menu.student_tb_menu()

def modify_stu_tb_schema():
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    print("---------------------- MODIFICATION MENU ----------------------------------------")
    print("1. Add a column\n2. Delete a column\n3. Rename a column\n"
          "4. Change datatype of the column\nb/B. Back to Dept. Menu\n"
          "q/Q. Exit")
    ch = input("\nEnter choice : ")

    # Add Column
    if ch == "1":
        col_name = input("Enter column name : ")
        col_datatype = input("Enter datatype of the column : ")
        query = f'''ALTER TABLE {data["student_tb"]}
                    ADD COLUMN {col_name} {col_datatype}'''

        cursor.execute(query)
        mydb.commit()

        print("-----------------------------------------------------------------------------")
        print(f"Column '{col_name}' added successfully...")

    # Drop Column
    if ch == "2":
        i = 1
        column_list = get_scheme(data["student_tb"])
        print("Select column to be deleted : ")
        for x in column_list:
            print(f"{i}.", x)
            i += 1
        column_pos = int(input("\nEnter column no. : "))
        column = column_list[column_pos - 1]
        query = f'''ALTER TABLE {data["student_tb"]}
                    DROP COLUMN {column} '''
        cursor.execute(query)
        mydb.commit()

        print("-----------------------------------------------------------------------------")
        print(f"Column '{column}' deleted successfully...")

    # Rename column
    if ch == "3":
        i = 1
        column_list = get_scheme(data["student_tb"])
        print("Select column to be renamed : ")
        for x in column_list:
            print(f"{i}.", x)
            i += 1
        column_pos = int(input("\nEnter column no. : "))
        column = column_list[column_pos - 1]
        col_name = input("Enter new column name : ")
        query = f'''ALTER TABLE {data["student_tb"]}
                            RENAME COLUMN {column} to {col_name} '''

        cursor.execute(query)
        mydb.commit()

        print("-----------------------------------------------------------------------------")
        print(f"Column '{col_name}' renamed successfully...")
        modify_stu_tb_schema()

    # changing the datatype of the column
    if ch == "4":
        i = 1
        column_list = get_scheme(data["student_tb"])
        print("Select column to change datatype : ")
        for x in column_list:
            print(f"{i}.", x)
            i += 1
        column_pos = int(input("\nEnter column no. : "))
        column = column_list[column_pos - 1]
        datatype = input(f"Enter new datatype of '{column}' : ")
        query = f'''ALTER TABLE {data["student_tb"]}
                    MODIFY COLUMN {column} {datatype}'''
        cursor.execute(query)
        mydb.commit()

        print("-----------------------------------------------------------------------------")
        print(f"Column '{column}' modified successfully...")
        modify_stu_tb_schema()

    if ch in ["b", "B"]:
        dept_menu.menu()

    if ch in ["q", "Q", "quit"]:
        print("-----------------------------------------------------------------------------")
        print("Thank you!!!")
        exit()

    # closing the connections
    cursor.close()
    mydb.close()
    modify_stu_tb_schema()

def insert_student_data(obj):
    """ It helps in inserting data of the student in the database
    :param obj: object of Student class
    :return: confirmation message
    """
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()
    # print(obj.__dict__)

    columns_name = ', '.join([key for key in obj.__dict__.keys()])
    format_specifier = ', '.join(["%s" for _ in obj.__dict__.values()])

    insert_query = f'''INSERT INTO {data["student_tb"]}
                       ({columns_name})
                       VALUES
                       ({format_specifier}) '''

    column_value = tuple([value for value in obj.__dict__.values()])

    cursor.execute(insert_query, column_value)
    mydb.commit()

    print("-------------------------- OUTPUT -------------------------------------------")
    print(cursor.rowcount, "rows affected...")

    # getting the student_id of the student whose details are inserted right now.
    print(f"Student id of {column_value[1]} : ", cursor.lastrowid)

    # closing the connections
    cursor.close()
    mydb.close()
    student_menu.menu()


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
    student_menu.menu()

def delete_stu_info(id):
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    fetch_query = f'''SELECT * FROM {data["student_tb"]}
                        WHERE student_id = {id}'''
    cursor.execute(fetch_query)
    details = cursor.fetchall()
    if len(details) < 1:
        print("-------------------------- OUTPUT -------------------------------------------")
        print("No records found...")
    else:
        print("-------------------------- OUTPUT -------------------------------------------")
        print("Details fetched...")
        print(details[0])
        ch = input("\nAre you want to delete this ? Press y/Y for 'Yes' or n/N for 'No' : ")

        if ch in ["y", "Y", "YES", "yes"]:
            query = f'''DELETE FROM {data["student_tb"]}
                        WHERE student_id = {id} '''

            cursor.execute(query)
            mydb.commit()
            print("-------------------------- OUTPUT -------------------------------------------")
            print(cursor.rowcount, " rows affected.")

    # closing the connections
    cursor.close()
    mydb.close()
    student_menu.menu()

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
            student_menu.menu()


    # closing the connections
    cursor.close()
    mydb.close()
    student_menu.menu()

def stu_all_info():
    # accessing user info
    data = get_basic_info()

    # establishing connection with the database
    mydb = make_connection(data)

    # preparing cursor object
    cursor = mydb.cursor()

    query = f'''SELECT * FROM {data["student_tb"]}'''
    cursor.execute(query)
    result = cursor.fetchall()

    print("-------------------------- OUTPUT -------------------------------------------")
    print(f"{len(data)} records found...")
    column_list = get_scheme(data["student_tb"])
    print(column_list)
    for stu_data in result:
        print("-----------------------------------------------------------------------------")
        print(stu_data)

    # closing the connections
    cursor.close()
    mydb.close()
    student_menu.menu()
