import flet as ft
import pymysql

# =======================
# CONFIG DB
# =======================
def db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="sistema_ayuda",
        port=3306,
        charset="utf8mb4"
    )

# =======================
# SESIÓN
# =======================
session = {"rol": None, "nombre": None, "grupo": None}

# =======================
# APP
# =======================
def main(page: ft.Page):
    page.title = "SchoolFlow"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0F19"
    page.padding = 0

    # ================= UI HELPERS =================
    def snack(msg):
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def card(content):
        return ft.Container(
            padding=20,
            border_radius=18,
            bgcolor="#111827",
            shadow=ft.BoxShadow(blur_radius=20, color="#00000040"),
            content=content
        )

    def field(label, icon, password=False):
        return ft.TextField(
            label=label,
            prefix_icon=icon,
            password=password,
            can_reveal_password=password,
            border_radius=14,
            bgcolor="#0F172A",
            border_color="transparent",
            focused_border_color="#6366F1",
            width=320
        )

    # ================= FIELDS =================
    user = field("Usuario", ft.Icons.PERSON)
    pw = field("Contraseña", ft.Icons.LOCK, True)

    name = field("Nombre", ft.Icons.BADGE)
    group = field("Grupo", ft.Icons.GROUP)
    new_user = field("Nuevo usuario", ft.Icons.ADD)
    new_pw = field("Nueva contraseña", ft.Icons.KEY, True)

    issue = ft.TextField(
        label="Describe el problema...",
        multiline=True,
        min_lines=3,
        border_radius=14,
        bgcolor="#0F172A",
        border_color="transparent",
        width=320
    )

    # ================= LOGIN =================
    def login(e):
        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                "SELECT rol, nombre, grupo FROM usuarios WHERE usuario=%s AND contrasena=%s",
                (user.value, pw.value)
            )

            r = cur.fetchone()
            con.close()

            if r:
                session["rol"], session["nombre"], session["grupo"] = r
                home()
            else:
                snack("Credenciales incorrectas")

        except Exception as e:
            snack(str(e))

    # ================= REGISTER =================
    role = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Alumno", label="Alumno"),
            ft.Radio(value="Profesor", label="Profesor")
        ]),
        value="Alumno"
    )

    def register(e):
        try:
            if not new_user.value or not new_pw.value or not name.value:
                snack("Completa todos los campos")
                return

            con = db()
            cur = con.cursor()

            cur.execute(
                "INSERT INTO usuarios (usuario, contrasena, rol, nombre, grupo) VALUES (%s,%s,%s,%s,%s)",
                (
                    new_user.value,
                    new_pw.value,
                    role.value,
                    name.value,
                    group.value if role.value == "Alumno" else "N/A"
                )
            )

            con.commit()
            con.close()

            snack("Cuenta creada")
            login_view(None)

        except Exception as e:
            snack(str(e))

    # ================= INCIDENT =================
    def send(e):
        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                "INSERT INTO incidencias (alumno, grupo, descripcion) VALUES (%s,%s,%s)",
                (session["nombre"], session["grupo"], issue.value)
            )

            con.commit()
            con.close()

            issue.value = ""
            snack("Enviado")
            home()

        except Exception as e:
            snack(str(e))

    def delete(id_):
        try:
            con = db()
            cur = con.cursor()

            cur.execute("DELETE FROM incidencias WHERE id=%s", (id_,))
            con.commit()
            con.close()

            snack("Resuelto")
            home()

        except Exception as e:
            snack(str(e))

    # ================= LOGIN UI =================
    def login_view(e):
        page.clean()

        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(["#0B0F19", "#111827"]),
                content=ft.Column(
                    alignment="center",
                    horizontal_alignment="center",
                    controls=[
                        ft.Icon(ft.Icons.SCHOOL, size=80, color="#6366F1"),
                        ft.Text("SchoolFlow", size=32, weight="bold"),
                        ft.Text("Sistema Escolar Inteligente", opacity=0.6),
                        user,
                        pw,
                        ft.ElevatedButton(
                            "Entrar",
                            on_click=login,
                            bgcolor="#6366F1",
                            color="white",
                            width=320
                        ),
                        ft.TextButton("Crear cuenta", on_click=register_view)
                    ]
                )
            )
        )

    # ================= REGISTER UI =================
    def register_view(e):
        page.clean()

        page.add(
            ft.Container(
                expand=True,
                gradient=ft.LinearGradient(["#0B0F19", "#111827"]),
                content=ft.Column(
                    alignment="center",
                    horizontal_alignment="center",
                    controls=[
                        ft.Text("Crear cuenta", size=30, weight="bold"),
                        role,
                        name,
                        group,
                        new_user,
                        new_pw,
                        ft.ElevatedButton(
                            "Registrar",
                            on_click=register,
                            bgcolor="#22C55E",
                            color="white",
                            width=320
                        ),
                        ft.TextButton("Volver", on_click=login_view)
                    ]
                )
            )
        )

    # ================= HOME =================
    def home():
        page.clean()

        if session["rol"] == "Alumno":

            def open(e):
                box.visible = True
                page.update()

            box = ft.Column([issue, ft.ElevatedButton("Enviar", on_click=send)], visible=False)

            page.add(
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(["#0B0F19", "#111827"]),
                    content=ft.Column(
                        alignment="center",
                        horizontal_alignment="center",
                        controls=[
                            card(ft.Column([
                                ft.Text(f"👤 {session['nombre']}", size=22),
                                ft.Text(f"Grupo: {session['grupo']}", opacity=0.7),
                                ft.ElevatedButton(
                                    "🚨 Solicitar ayuda",
                                    on_click=open,
                                    bgcolor="red",
                                    color="white",
                                    width=320
                                ),
                                box,
                                ft.TextButton("Cerrar sesión", on_click=login_view)
                            ]))
                        ]
                    )
                )
            )

        else:
            con = db()
            cur = con.cursor()

            cur.execute("SELECT id, alumno, grupo, descripcion FROM incidencias ORDER BY id DESC")
            data = cur.fetchall()
            con.close()

            items = []

            for d in data:
                items.append(
                    card(ft.Column([
                        ft.Text(d[1], weight="bold"),
                        ft.Text(f"Grupo: {d[2]}", opacity=0.7),
                        ft.Text(d[3]),
                        ft.ElevatedButton(
                            "Resolver",
                            on_click=lambda e, id=d[0]: delete(id),
                            bgcolor="#22C55E",
                            color="white"
                        )
                    ]))
                )

            page.add(
                ft.Container(
                    expand=True,
                    gradient=ft.LinearGradient(["#0B0F19", "#111827"]),
                    content=ft.Column([
                        ft.Text("Panel Profesor", size=26),
                        ft.Column(items, scroll="auto", expand=True),
                        ft.TextButton("Cerrar sesión", on_click=login_view)
                    ])
                )
            )

        page.update()

    login_view(None)


if __name__ == "__main__":
    ft.app(target=main)