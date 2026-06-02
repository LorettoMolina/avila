import flet as ft

def LoginView(page, login_func, register_view):

    user = ft.TextField(
        label="Usuario",
        prefix_icon=ft.Icons.PERSON,
        width=320
    )

    pw = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True,
        width=320
    )

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.SCHOOL, size=80),
                ft.Text("SchoolFlow", size=32, weight="bold"),
                user,
                pw,
                ft.ElevatedButton(
                    "Entrar",
                    on_click=lambda e: login_func(
                        user.value,
                        pw.value
                    )
                ),
                ft.TextButton(
                    "Crear cuenta",
                    on_click=register_view
                )
            ]
        )
    )