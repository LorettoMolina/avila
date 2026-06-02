import flet as ft

def AlumnoView(page, nombre, grupo, send_func, logout):

    incidencia = ft.TextField(
        label="Describe el problema",
        multiline=True,
        width=320
    )

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    f"👤 {nombre}",
                    size=22
                ),

                ft.Text(
                    f"Grupo: {grupo}"
                ),

                incidencia,

                ft.ElevatedButton(
                    "🚨 Solicitar ayuda",
                    on_click=lambda e: send_func(
                        incidencia.value
                    )
                ),

                ft.TextButton(
                    "Cerrar sesión",
                    on_click=logout
                )
            ]
        )
    )