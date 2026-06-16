import pymysql


def db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_ayuda",
        port=3306,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor
    )