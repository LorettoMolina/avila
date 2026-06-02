from models.databaseModel import db

class UserModel:

    @staticmethod
    def login(usuario, contrasena):
        con = db()
        cur = con.cursor()

        cur.execute(
            "SELECT rol,nombre,grupo FROM usuarios WHERE usuario=%s AND contrasena=%s",
            (usuario, contrasena)
        )

        data = cur.fetchone()
        con.close()

        return data

    @staticmethod
    def register(usuario, contrasena, rol, nombre, grupo):
        con = db()
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO usuarios
            (usuario,contrasena,rol,nombre,grupo)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (usuario, contrasena, rol, nombre, grupo)
        )

        con.commit()
        con.close()