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


def login(username, password, db):
    query = "select distinct Password from student where Name=\'" + str(username) + "\'"
    success = db.execute(query)
    data = db.fetchall()
    if success:
        for item in data:
            if item['Password'] == password:
                return True
    return False


def main():
    # Initiate the database
    with DB() as db:
        # Initiate the interface
        print("Hi, here is the login interface\n")

        while True:
            username = input("Please type your username: \n")
            password = input("Please type your password: \n")

            if not login(username, password, db):
                print("Log in failed, please try again")
            else:
                print("\nHi, here is the Student Menu\n")
                break







if __name__ == "__main__":
    main()