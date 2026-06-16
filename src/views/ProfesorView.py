import flet as ft


def ProfesorView(
    page,
    incidencias,
    resolver_func,
    logout
):

    lista = []

    for item in incidencias:

        lista.append(

            ft.Card(

                content=ft.Container(

                    padding=15,

                    content=ft.Column([

                        ft.Text(
                            item["alumno"]
                        ),

                        ft.Text(
                            item["grupo"]
                        ),

                        ft.Text(
                            item["descripcion"]
                        ),

                        ft.ElevatedButton(

                            "Resolver",

                            on_click=lambda e,
                            id=item["id_incidencia"]:
                            resolver_func(id)

                        )
                    ])
                )
            )
        )

    return ft.Column(

        expand=True,

        controls=[

            ft.Text(
                "Panel Profesor",
                size=30
            ),

            ft.Column(
                lista,
                expand=True,
                scroll="auto"
            ),

            ft.TextButton(
                "Cerrar sesión",
                on_click=logout
            )
        ]
    )