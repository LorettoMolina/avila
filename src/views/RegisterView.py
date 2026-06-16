import flet as ft


def RegisterView(page, register_func, login_view):

    nombre = ft.TextField(
        label="Nombre",
        width=320
    )

    grupo = ft.TextField(
        label="Grupo",
        width=320
    )

    usuario = ft.TextField(
        label="Usuario",
        width=320
    )

    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=320
    )

    rol = ft.RadioGroup(

        value="Alumno",

        content=ft.Row([

            ft.Radio(
                value="Alumno",
                label="Alumno"
            ),

            ft.Radio(
                value="Profesor",
                label="Profesor"
            )

        ])
    )

    def cambiar(e):

        grupo.visible = (
            rol.value == "Alumno"
        )

        page.update()

    rol.on_change = cambiar

    def registrar(e):

        register_func(

            usuario.value,

            password.value,

            rol.value,

            nombre.value,

            grupo.value
            if rol.value == "Alumno"
            else "Docente"
        )

    return ft.Container(

        expand=True,

        content=ft.Column(

            alignment=ft.MainAxisAlignment.CENTER,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text(
                    "Crear cuenta",
                    size=30
                ),

                rol,

                nombre,

                grupo,

                usuario,

                password,

                ft.ElevatedButton(
                    "Registrar",
                    on_click=registrar
                ),

                ft.TextButton(
                    "Volver",
                    on_click=login_view
                )

            ]
        )
    )