class UserController:

    @staticmethod
    def login(usuario, contrasena):

        if not usuario or not contrasena:
            return None

        return UserModel.login(
            usuario,
            contrasena
        )

    @staticmethod
    def register(usuario, contrasena, rol, nombre, grupo):

        if not all([
            usuario,   
            contrasena,
            rol,
            nombre,
            grupo
        ]):
            return False

        return UserModel.register(
            usuario,
            contrasena,
            rol,
            nombre,  
            grupo
        )