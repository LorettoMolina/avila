import flet as ft


def AlumnoView(
    page,
    nombre,
    grupo,
    send_func,
    logout
):

    incidencia = ft.TextField(

        label="Describe el problema",

        multiline=True,

        width=320
    )

    def enviar(e):

        if not incidencia.value:

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Escribe una incidencia"
                )
            )

            page.snack_bar.open = True

            page.update()

            return

        send_func(
            incidencia.value
        )

        incidencia.value = ""

        page.update()

    return ft.Container(

        expand=True,

        content=ft.Column(

            alignment=ft.MainAxisAlignment.CENTER,

            horizontal_alignment=ft.CrossAxisAlignment.CENTER,

            controls=[

                ft.Text(
                    f"👤 {nombre}",
                    size=24
                ),

                ft.Text(
                    f"Grupo: {grupo}"
                ),

                incidencia,

                ft.ElevatedButton(

                    "🚨 Solicitar ayuda",

                    on_click=enviar
                ),

                ft.TextButton(

                    "Cerrar sesión",

                    on_click=logout
                )
            ]
        )
    )