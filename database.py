import mysql.connector
import os


# db = None

def connection():
    return mysql.connector.connect(
	host = os.environ.get("PSWDHOST"),
	user = os.environ.get("PSWDUSERNAME"),
	passwd = os.environ.get("PSWDPASSWORD"),
	database = os.environ.get("PSWDDATABASE")
	)


def write_todb(db,user,password,email):
    taken = False
    query = "INSERT INTO Users(user,password,email) VALUES(%s,%s,%s)"
    cursor = db.cursor()

    cursor.execute("SELECT user FROM Users WHERE user=%s",(user,))

    for obj in cursor:
        if obj[0] == user:
            taken = True
    
    if taken:
        return "401"
    else:
        cursor.execute(query,(user,password,email))
        db.commit()
        return "200"


def read_todb(db,user,password):
    query = "SELECT password FROM Users WHERE user=%s"
    cursor = db.cursor()
    cursor.execute(query,(user,))
    user_password = None

    for obj in cursor:
        user_password = obj[0]
    
    if not user_password:
        return "404"
    else:
        if user_password == password:
            return "200"
        else:
            return "401"

    
