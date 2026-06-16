from models.IncidenciaModel import IncidenciaModel

class IncidenciaController:

    @staticmethod
    def crear(
        alumno,
        grupo,
        descripcion
    ):

        return IncidenciaModel.crear(
            alumno,
            grupo,
            descripcion
        )

    @staticmethod
    def obtener():

        return IncidenciaModel.obtener() 

    @staticmethod
    def eliminar(id_):

        return IncidenciaModel.eliminar(
            id_
        )