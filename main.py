import time
import pymysql


class DB():
    def __init__(self, host='localhost', port=3306, db='project3-nudb', user='root', passwd='Zhihan1996', charset='utf8'):
        self.connect = pymysql.connect(host=host, port=port, db=db, user=user, passwd=passwd, charset=charset)
        self.cur = self.connect.cursor(cursor = pymysql.cursors.DictCursor)

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connect.commit()
        self.cur.close()
        self.connect.close()

def year_quarter():
    localtime = time.localtime(time.time())
    year = localtime.tm_year
    month = localtime.tm_mon
    quarter = "Q1" if month < 7 else "Q2"

    return year, quarter


def next_quarter(year, quarter):
    if quarter == "Q2":
        year += 1
        quarter = "Q1"
    else:
        quarter = "Q2"

    return year, quarter

def check_login(username, password, db):
    query = "select distinct Password " \
            "from student " \
            "where Name=\'" + str(username) + "\'"
    success = db.execute(query)
    if success:
        data = db.fetchall()
        for item in data:
            if item['Password'] == password:
                return True
    return False



def login(db):
    welcome = "Hi, here is the login interface\n"
    print("-"*60)
    print(welcome)
    while True:
        username = input("Please type your username: \n")
        print("\n")
        password = input("Please type your password: \n")

        if not check_login(username=username, password=password, db=db):
            print("\nLog in failed, please try again\n")
        else:
            # find out the student's id
            id_query = "select distinct Id " \
                       "from student " \
                       "where Name=" + "\'" + str(username) + "\'"
            db.execute(id_query)
            data = db.fetchall()
            sid = data[0]["Id"]
            menu(db=db, sid=sid, username=username)


def menu(db, sid, username):
    welcome = "Hi, here is the Student Menu"
    print("\n" + "-"*60)
    print(welcome)
    print("You courses are listed as follow:\n")

    # Construct query
    year, quarter = year_quarter()

    query = "select distinct UoSCode " \
            "from student, transcript " \
            "where student.Id=transcript.StudId " \
            "and Year=" + str(year) +" " \
            "and Semester=" + "\'" + str(quarter) + "\'" + " " \
            "and student.Name=" + "\'" + str(username) + "\'"


    # Query the result and print it
    success = db.execute(query)
    if success:
        data = db.fetchall()
        for item in data:
            print("="*len(item["UoSCode"]))
            print(item["UoSCode"])
        print("=" * len(item["UoSCode"]))



    choose(db, sid, username)



def transcript(db, sid, username):
    welcome = "Hi, here is the Transcript Interface"
    print("\n" + "-" * 60)
    print(welcome)
    print("You courses and corresponding grades are listed as follow:\n")

    # print the courses and grades
    success = db.callproc('transc', args=[sid])
    if success:
        data = db.fetchall()
        # print out the results
        print("COURSE    GRADA")
        print("=" * len("COURSE    GRADA"))
        for item in data:
            information = str(item["UoSCode"]) + "  " + str(item["Grade"])
            print(information)
        print("=" * len("COURSE    GRADA"))


    while True:
        print("If you want to come back, type 1")
        print("For course detail, type the course number\n\n")
        choice = input("Your choice: ")
        if choice == str(1):
            menu(db, sid, username)
        else:
            db.callproc('transcript_details', args=[sid, choice])
            data = db.fetchall()
            if len(data) == 0:
                print("\nPlease type a correct input")
            else:
                data = data[0]
                print("\nCourse Number: " + str(data["UoSCode"]))
                print("Course Title: " + str(data["UoSName"]))
                print("Course Year: " + str(data["Year"]))
                print("Course Quarter: " + str(data["Semester"]))
                print("Course Enroll: " + str(data["Enrollment"]))
                print("Max Enroll: " + str(data["MaxEnrollment"]))
                print("Course Lecturer: " + str(data["Name"]))
                print("Course Grade: " + str(data["Grade"]) + "\n")


def enroll(db, sid, username):
    welcome = "Hi, here is the Enroll Interface"
    print("\n" + "-" * 60)
    print(welcome)
    print("All the courses are listed as follow:\n")

    year, quarter = year_quarter()

    # find all the courses that are available now
    all_course_name_list = []
    all_course_list = []
    # current quarter
    db.callproc('find_enroll_all', args=[sid, year, quarter])
    data = db.fetchall()
    for item in data:
        course = str(item["UoSCode"]) + "  " + str(item["UoSName"])
        all_course_list.append(str(item["UoSCode"]))
        all_course_name_list.append(course)

    # next quarter
    year, quarter = next_quarter(year, quarter)

    db.callproc('find_enroll_all', args=[sid, year, quarter])
    data = db.fetchall()
    for item in data:
        course = str(item["UoSCode"]) + "  " + str(item["UoSName"])
        if course not in all_course_name_list:
            all_course_list.append(str(item["UoSCode"]))
            all_course_name_list.append(course)

    # print all courses
    for course in all_course_name_list:
        print(course + "\n")

    # Interact
    while True:
        print("\nWhich course are you interested in enrolling? \n "
              "Type 1 to come back.\n"
              "Or type the course number\n")
        course = input("Your choice > ")

        if course == str(1):
            menu(db, sid, username)
        elif course not in all_course_list:
            print("Please type a valid course number")
        else:
            # find all the course that are available for the student
            year, quarter = year_quarter()
            db.callproc('find_enroll', args=[sid, year, quarter])
            data = db.fetchall()
            ava_course_list = []
            for item in data:
                ava_course_list.append(item["UoSCode"])

            year, quarter = next_quarter(year, quarter)

            db.callproc('find_enroll', args=[sid, year, quarter])
            data = db.fetchall()
            for item in data:
                if item["UoSCode"] not in ava_course_list:
                    ava_course_list.append(item["UoSCode"])


            # determine the reason
            if course in ava_course_list:
                db.callproc('enroll_class', args=[sid, course, year, quarter])
                print("Successfully enroll in " + course)
            else:
                year, quarter = year_quarter()
                query = "select UoSCode, Enrollment, MaxEnrollment " \
                        "from uosoffering " \
                        "where UoSCode=" + '\'' + course + '\'' + " " \
                        "and Semester=" + "\'" + str(quarter) + "\'" + " " \
                        "and Year=" + "\'" + str(year) + "\'"
                db.execute(query)
                data = db.fetchall()[0]
                if int(data["MaxEnrollment"]) <= int(data["Enrollment"]):
                    print("This course is full")
                else:
                    print("Your have not cleared the prerequisites")
                    # find the prerequisite
                    db.callproc('find_enroll_all', args=[sid, year, quarter])
                    all_data = db.fetchall()
                    for item in all_data:
                        if item["UoSCode"] == course:
                            prerequisite = item["PrereqUoSCode"]
                    print("There is the prerequisite: \n")
                    print(prerequisite)
                    print("\n")






def withdraw(db, sid, username):
    print("\n" + '-' * 60)
    print("Here is the withdraw page.\n")

    year, quarter = year_quarter()

    # Find the courses that could be withdrawed
    db.callproc('able_withdraw', args=[sid, year, quarter])
    data = db.fetchall()
    course_number_list = []
    course_list = []
    if len(data) != 0:
        for item in data:
            course = [item["UoSCode"], item["Year"], item["Semester"]]
            course_number_list.append(item["UoSCode"])
            course_list.append(course)
            print("Course Number: " + str(item["UoSCode"]))
            print("Course Title: " + str(item["UoSName"]))
            print("Course Year: " + str(item["Year"]))
            print("Course Quarter: " + str(item["Semester"]) + "\n")

    year, quarter = next_quarter(year, quarter)
    db.callproc('able_withdraw', args=[sid, year, quarter])
    data = db.fetchall()
    if len(data) != 0:
        for item in data:
            course = [item["UoSCode"], item["Year"], item["Semester"]]
            if course not in course_list:
                course_number_list.append(item["UoSCode"])
                course_list.append(course)
                print("Course Number: " + str(item["UoSCode"]))
                print("Course Title: " + str(item["UoSName"]))
                print("Course Year: " + str(item["Year"]))
                print("Course Quarter: " + str(item["Semester"]) + "\n")


    # Withdraw a course

    while True:
        print("Please type in the number of the course you want to withdraw.")
        print("Or type 1 to come back")
        course = input("Course to withdraw > ")

        if course == "1":
            menu(db, sid, username)

        year = input("Which year > ")
        quarter = input("Which quarter > ")

        if course in course_number_list:
            db.callproc('withdraw_class', args=[sid, course, year, quarter])
            # detect the trigger
            query = "select c " \
                    "from monitor " \
                    "where item=\'mon\'"
            db.execute(query)
            data = db.fetchall()[0]['c']

            if data == str(1):
                print("!" * 50)
                print("Enrolled number less than half of the maxenroll")
                print("!" * 50)

            print("Withdraw finish")
            # menu(db, sid, username)
        else:
            print("Please choose a valid course\n")




def person(db, sid, username):
    print("\n" + '-'*60)
    print("Here is the personal information page.")

    query = "select * " \
            "from student " \
            "where Name=\'" + str(username) + "\'"
    db.execute(query)
    data = db.fetchall()[0]
    print("\nID: " + str(data["Id"]))
    print("Name: " + str(data["Name"]))
    print("Password: " + str(data["Password"]))
    print("Address: " + str(data["Address"]) + "\n")

    print("You could change your password and address here.")

    while True:
        password = input("Please type you password > ")
        address = input("Please type you address > ")
        try:
            db.callproc('personal_update', args=[sid, password, address])
            print("Update success")
            menu(db, sid, username)
        except:
            print("\nUpdate fails")
            print("Length of password should be less than 10")
            print("Length of address should be less than 50\n")


def choose(db, sid, username):
    # List the choices
    print("\nYou have several options:")
    print("Type 1 for Transcript")
    print("Type 2 for Enroll")
    print("Type 3 for Withdraw")
    print("Type 4 for Personal Details")
    print("Type 5 for Logout\n")
    choice = input("Your choice: ")

    if choice == str(1):
        transcript(db, sid, username)
    elif choice == str(2):
        enroll(db, sid, username)
    elif choice == str(3):
        withdraw(db, sid, username)
    elif choice == str(4):
        person(db, sid, username)
    elif choice == str(5):
        print("Successfully logout\n")
        login(db)
    else:
        print("Please type in a integer between 1 and 5")
        choose(db, sid, username)



def main():
    # Initiate the database
    with DB() as db:
        # Initiate the procedure
        login(db=db)



if __name__ == "__main__":
    main()