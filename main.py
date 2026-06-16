import flet as ft

from controllers.UserController import UserController
from controllers.IncidenciaController import IncidenciaController

from views.LoginView import LoginView
from views.RegisterView import RegisterView
from views.AlumnoView import AlumnoView
from views.ProfesorView import ProfesorView


def main(page: ft.Page):

    page.title = "SchoolFlow"

    usuario_actual = {}

    def mensaje(texto):

        page.snack_bar = ft.SnackBar(
            ft.Text(texto)
        )

        page.snack_bar.open = True

        page.update()

    def abrir_login(e=None):

        page.clean()

        page.add(
            LoginView(
                page,
                login,
                abrir_register
            )
        )

        page.update()

    def abrir_register(e=None):

        page.clean()

        page.add(
            RegisterView(
                page,
                register,
                abrir_login
            )
        )

        page.update()

    def register(
        usuario,
        password,
        rol,
        nombre,
        grupo
    ):

        ok = UserController.register(
            usuario,
            password,
            rol,
            nombre,
            grupo
        )

        if ok:

            mensaje("Cuenta creada correctamente")

            abrir_login()

        else:

            mensaje("Usuario ya existe")

    def login(
        usuario,
        password
    ):

        data = UserController.login(
            usuario,
            password
        )

        if not data:

            mensaje(
                "Usuario o contraseña incorrecta"
            )

            return

        usuario_actual.update(data)

        mensaje(
            f'Bienvenido {data["nombre"]}'
        )

        if data["rol"] == "Alumno":

            abrir_alumno()

        else:

            abrir_profesor()

    def abrir_alumno():

        page.clean()

        page.add(

            AlumnoView(

                page,

                usuario_actual["nombre"],

                usuario_actual["grupo"],

                enviar,

                abrir_login
            )
        )

        page.update()

    def abrir_profesor():

        page.clean()

        page.add(

            ProfesorView(

                page,

                IncidenciaController.obtener(),

                resolver,

                abrir_login
            )
        )

        page.update()

    def enviar(texto):

        ok = IncidenciaController.crear(

            usuario_actual["nombre"],

            usuario_actual["grupo"],

            texto
        )

        if ok:

            mensaje(
                "Solicitud enviada"
            )

        else:

            mensaje(
                "No se pudo enviar"
            )

    def resolver(id_):

        IncidenciaController.eliminar(
            id_
        )

        mensaje(
            "Incidencia resuelta"
        )

        abrir_profesor()

    abrir_login()


ft.app(target=main)