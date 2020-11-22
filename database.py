import mysql.connector
import os
import bcrypt
from cryptography.fernet import Fernet


key = os.environ.get("ENCRYPTKEY")

# db = None


def connection():
    return mysql.connector.connect(
        host=os.environ.get("PSWDHOST"),
        user=os.environ.get("PSWDUSERNAME"),
        passwd=os.environ.get("PSWDPASSWORD"),
        database=os.environ.get("PSWDDATABASE")
    )


def write_todb(db, user, password, email):
    taken = False
    query = "INSERT INTO Users(user,password,email) VALUES(%s,%s,%s)"
    cursor = db.cursor()

    cursor.execute("SELECT user FROM Users WHERE user=%s", (user,))

    for obj in cursor:
        if obj[0] == user:
            taken = True

    if taken:
        return "401"
    else:
        hashed_password = bcrypt.hashpw(
            password.encode("UTF-8"), bcrypt.gensalt())
        cursor.execute(query, (user, hashed_password.decode("UTF-8"), email))
        db.commit()
        return "200"


def read_todb(db, user, password):
    query = "SELECT password FROM Users WHERE user=%s"
    cursor = db.cursor()
    cursor.execute(query, (user,))
    user_password = None

    for obj in cursor:
        user_password = obj[0]

    if not user_password:
        return "404"
    else:
        if bcrypt.checkpw(password.encode("UTF-8"), user_password.encode("UTF-8")):
            return "200"
        else:
            return "401"


def write_tocreddb(db, password, user, username=None, email=None, phone=None, url=None):
    query = "INSERT INTO Credentials(username,email,phone,url,password,user) VALUES(%s,%s,%s,%s,%s,%s)"
    cipher = Fernet(key.encode("UTF-8"))
    cursor = db.cursor()
    cursor.execute(query, (username, email, phone, url,
                           cipher.encrypt(password.encode("UTF-8")), user))
    db.commit()


def read_tocreddb(db, user):
    query = "SELECT id,username,email,phone,url,password FROM Credentials WHERE user=%s"

    cipher = Fernet(key.encode("UTF-8"))

    cursor = db.cursor()

    cursor.execute(query, (user,))

    results = []

    for obj in cursor:
        dicto = {}
        dicto['id'] = obj[0]
        dicto['username'] = obj[1]
        dicto['email'] = obj[2]
        dicto['phone'] = obj[3]
        dicto['url'] = obj[4]
        dicto['password'] = cipher.decrypt(obj[5].encode("UTF-8"))

        results.append(dicto)

    return results


def delete_tocreddb(db, id):
    query = "DELETE FROM Credentials where id=%s"

    cursor = db.cursor()
    cursor.execute(query, (id,))

    db.commit()


def update_tocreddb(db, id, username, email, phone, url, password):
    query = "UPDATE Credentials SET username=%s,email=%s,phone=%s,url=%s,password=%s WHERE id=%s"
    cipher = Fernet(key.encode("UTF-8"))
    cursor = db.cursor()
    cursor.execute(query, (username, email, phone, url,
                           cipher.encrypt(password.encode("UTF-8")), id))

    db.commit()
