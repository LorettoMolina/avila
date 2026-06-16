import flet as ft


def LoginView(page, login_func, register_view):

    user = ft.TextField(
        label="Usuario",
        width=320
    )

    pw = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=320
    )

    def entrar(e):

        login_func(
            user.value,
            pw.value
        )

    return ft.Container(

        expand=True,

        content=ft.Column(

            alignment=ft.MainAxisAlignment.CENTER,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Icon(
                    ft.Icons.SCHOOL,
                    size=80
                ),

                ft.Text(
                    "SchoolFlow",
                    size=32
                ),

                user,

                pw,

                ft.ElevatedButton(
                    "Entrar",
                    on_click=entrar
                ),

                ft.TextButton(
                    "Crear cuenta",
                    on_click=register_view
                )
            ]
        )
    )