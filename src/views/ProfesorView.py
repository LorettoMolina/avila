import flet as ft

def ProfesorView(page, incidencias, resolver_func, logout):

    cards = []

    for item in incidencias:

        cards.append(
            ft.Container(
                padding=15,
                border_radius=10,
                bgcolor="#111827",

                content=ft.Column([
                    ft.Text(
                        item[1],
                        weight="bold"
                    ),

                    ft.Text(
                        f"Grupo: {item[2]}"
                    ),

                    ft.Text(
                        item[3]
                    ),

                    ft.ElevatedButton(
                        "Resolver",
                        on_click=lambda e,
                        id=item[0]:
                        resolver_func(id)
                    )
                ])
            )
        )

    return ft.Container(
        expand=True,
        content=ft.Column(
            expand=True,
            controls=[
                ft.Text(
                    "Panel Profesor",
                    size=26
                ),

                ft.Column(
                    cards,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True
                ),

                ft.TextButton(
                    "Cerrar sesión",
                    on_click=logout
                )
            ]
        )
    )