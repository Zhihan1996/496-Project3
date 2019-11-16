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
    while True:
        username = input("Please type your username: \n")
        print("\n")
        password = input("Please type your password: \n")

        if not check_login(username=username, password=password, db=db):
            print("Log in failed, please try again")
        else:
            return username

def menu(db, username):
    print("\nHi, here is the Student Menu")
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

    # List the choices
    print("\nYou have several options:")
    print("Type 1 for Transcript")
    print("Type 2 for Enroll")
    print("Type 3 for Withdraw")
    print("Type 4 for Personal Details")
    print("Type 5 for Logout\n")
    choice = input("Your choice: ")

    return choice


    

def main():
    # Initiate the database
    with DB() as db:
        # Initiate the interface
        print("Hi, here is the login interface\n")

        # Login
        username = login(db=db)
        choice = menu(username=username,db=db)





if __name__ == "__main__":
    main()