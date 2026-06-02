from models.databaseModel import db

class IncidenciaModel:

    @staticmethod
    def crear(alumno, grupo, descripcion):
        con = db()
        cur = con.cursor()

        cur.execute(
            """
            INSERT INTO incidencias
            (alumno,grupo,descripcion)
            VALUES (%s,%s,%s)
            """,
            (alumno, grupo, descripcion)
        )

        con.commit()
        con.close()

    @staticmethod
    def obtener():
        con = db()
        cur = con.cursor()

        cur.execute(
            """
            SELECT id,alumno,grupo,descripcion
            FROM incidencias
            ORDER BY id DESC
            """
        )

        data = cur.fetchall()
        con.close()

        return data

    @staticmethod
    def eliminar(id_):
        con = db()
        cur = con.cursor()

        cur.execute(
            "DELETE FROM incidencias WHERE id=%s",
            (id_,)
        )

        con.commit()
        con.close()