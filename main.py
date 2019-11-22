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

    # Find local time and construct query
    localtime = time.localtime(time.time())
    year = localtime.tm_year
    month = localtime.tm_mon
    semester = "Q1" if month < 7 else "Q2"
    query = "select distinct UoSCode " \
            "from student, transcript " \
            "where student.Id=transcript.StudId " \
            "and Year=" + str(year) +" " \
            "and Semester=" + "\'" + str(semester) + "\'" + " " \
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
                print("Course Grade: " + str(data["Grade"] + "\n"))






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
        pass
    elif choice == str(3):
        pass
    elif choice == str(4):
        pass
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