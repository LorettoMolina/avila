import flet as ft

def RegisterView(page, register_func, login_view):

    nombre = ft.TextField(label="Nombre", width=320)
    grupo = ft.TextField(label="Grupo", width=320)
    usuario = ft.TextField(label="Usuario", width=320)

    password = ft.TextField(
        label="Contraseña",
        password=True,
        width=320
    )

    rol = ft.RadioGroup(
        value="Alumno",
        content=ft.Row([
            ft.Radio(value="Alumno", label="Alumno"),
            ft.Radio(value="Profesor", label="Profesor")
        ])
    )

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    "Crear cuenta",
                    size=30,
                    weight="bold"
                ),
                rol,
                nombre,
                grupo,
                usuario,
                password,
                ft.ElevatedButton(
                    "Registrar",
                    on_click=lambda e: register_func(
                        usuario.value,
                        password.value,
                        rol.value,
                        nombre.value,
                        grupo.value
                    )
                ),
                ft.TextButton(
                    "Volver",
                    on_click=login_view
                )
            ]
        )
    )