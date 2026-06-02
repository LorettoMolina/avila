from models.UserModel import UserModel

class UserController:

    @staticmethod
    def login(usuario, contrasena):
        return UserModel.login(usuario, contrasena)

    @staticmethod
    def register(usuario, contrasena, rol, nombre, grupo):
        UserModel.register(
            usuario,
            contrasena,
            rol,
            nombre,
            grupo
        )