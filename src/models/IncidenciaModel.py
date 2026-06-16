from models.databaseModel import db


class IncidenciaModel:

    @staticmethod
    def crear(alumno, grupo, descripcion):

        con = db()

        try:
            cur = con.cursor()

            sql = """
            INSERT INTO incidencias
            (alumno, grupo, descripcion)
            VALUES (%s, %s, %s)
            """

            cur.execute(
                sql,
                (alumno, grupo, descripcion)
            )

            con.commit()

            return True

        except Exception as e:
            print("Error:", e)
            return False

        finally:
            con.close()

    @staticmethod
    def obtener():

        con = db()

        try:

            cur = con.cursor()

            cur.execute("""
                SELECT
                id_incidencia,
                alumno,
                grupo,
                descripcion,
                fecha
                FROM incidencias
                ORDER BY id_incidencia DESC
            """)

            return cur.fetchall()

        except Exception as e:

            print("Error:", e)
            return []

        finally:

            con.close()

    @staticmethod
    def eliminar(id_):

        con = db()

        try:

            cur = con.cursor()

            cur.execute(  
                """
                DELETE FROM incidencias
                WHERE id_incidencia=%s
                """,
                (id_,)
            )

            con.commit()

            return True
  
        except Exception as e:

            print("Error:", e)
            return False

        finally:

            con.close()