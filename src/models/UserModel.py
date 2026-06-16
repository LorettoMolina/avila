from models.databaseModel import db


class UserModel:

    @staticmethod
    def login(usuario, contrasena):

        con = db()

        try:

            cur = con.cursor()

            cur.execute(
                """
                SELECT
                id_usuario,
                rol,
                nombre,
                grupo
                FROM usuarios
                WHERE usuario=%s
                AND contrasena=%s
                """,
                (usuario, contrasena)
            )

            usuario_encontrado = cur.fetchone()

            return usuario_encontrado

        except Exception as e:

            print("Error login:", e)
            return None

        finally:

            con.close()

    @staticmethod
    def register(usuario, contrasena, rol, nombre, grupo):

        con = db()

        try:

            cur = con.cursor()

            # validar usuario repetido
            cur.execute(
                """
                SELECT id_usuario
                FROM usuarios
                WHERE usuario=%s
                """,
                (usuario,)
            )

            existe = cur.fetchone()

            if existe:
                return False

            cur.execute(
                """
                INSERT INTO usuarios
                (
                    usuario,
                    contrasena,
                    rol,
                    nombre,
                    grupo
                )
                VALUES
                (%s,%s,%s,%s,%s)
                """,
                (
                    usuario,
                    contrasena,  
                    rol,
                    nombre,
                    grupo
                )
            )

            con.commit()

            return True
   
        except Exception as e:

            print("Error registro:", e)

            return False

        finally:

            con.close()