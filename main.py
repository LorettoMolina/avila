import flet as ft
import sqlite3

# --- Variables Globales para sustituir la Sesión ---
usuario_logeado = {
    "rol": "",
    "nombre": "",
    "grupo": ""
}

conn = sqlite3.connect("sistema_ayuda.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE,
                    contrasena TEXT,
                    rol TEXT,
                    nombre TEXT,
                    grupo TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS incidencias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    alumno TEXT,
                    grupo TEXT,
                    descripcion TEXT)''')
conn.commit()

def main(page: ft.Page):
    page.title = "Sistema de Incidencias"
    page.window_width = 450
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def iniciar_sesion(e):
        global usuario_logeado
        cursor.execute("SELECT rol, nombre, grupo FROM usuarios WHERE usuario=? AND contrasena=?", 
                       (txt_usuario.value, txt_pass.value))
        usuario = cursor.fetchone()
        if usuario:
            # Guardamos los datos en la variable global de forma segura
            usuario_logeado["rol"] = usuario[0]
            usuario_logeado["nombre"] = usuario[1]
            usuario_logeado["grupo"] = usuario[2]
            mostrar_pantalla_principal()
        else:
            lbl_error.value = "Usuario o contraseña incorrectos"
            lbl_error.update()

    def registrar_usuario(e):
        if not txt_reg_usuario.value or not txt_reg_pass.value or not txt_nombre.value:
            mostrar_alerta("Error", "Llena los campos obligatorios.")
            return
        rol = "Alumno" if rb_rol.value == "Alumno" else "Profesor"
        grupo_valor = txt_grupo.value if rol == "Alumno" else "N/A"
        try:
            cursor.execute("INSERT INTO usuarios (usuario, contrasena, rol, nombre, grupo) VALUES (?, ?, ?, ?, ?)",
                           (txt_reg_usuario.value, txt_reg_pass.value, rol, txt_nombre.value, grupo_valor))
            conn.commit()
            txt_reg_usuario.value = ""
            txt_reg_pass.value = ""
            txt_nombre.value = ""
            txt_grupo.value = ""
            mostrar_alerta("Exito", "Registrado correctamente.")
            mostrar_login(None)
        except sqlite3.IntegrityError:
            mostrar_alerta("Error", "El usuario ya existe.")

    def guardar_incidencia(e):
        if not txt_incidencia.value:
            mostrar_alerta("Aviso", "Escribe una descripcion.")
            return
        cursor.execute("INSERT INTO incidencias (alumno, grupo, descripcion) VALUES (?, ?, ?)",
                       (usuario_logeado["nombre"], usuario_logeado["grupo"], txt_incidencia.value))
        conn.commit()
        mostrar_alerta("Enviado", "Incidencia registrada.")
        txt_incidencia.value = ""
        mostrar_pantalla_principal()

    def cambiar_visibilidad_grupo(e):
        txt_grupo.visible = True if rb_rol.value == "Alumno" else False
        page.update()

    def mostrar_alerta(titulo, mensaje):
        def cerrar_dialogo(e):
            dlg.open = False
            page.update()
        dlg = ft.AlertDialog(
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[ft.TextButton("Ok", on_click=cerrar_dialogo)]
        )
        page.overlay.append(dlg)
        dlg.open = True
        page.update()

    def mostrar_login(e):
        page.clean()
        txt_usuario.value = ""
        txt_pass.value = ""
        lbl_error.value = ""
        page.add(
            ft.Column([
                ft.Text("Inicio de Sesion", size=26, weight=ft.FontWeight.BOLD),
                txt_usuario, 
                txt_pass,
                ft.ElevatedButton("Entrar", on_click=iniciar_sesion, width=250, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE),
                ft.TextButton("Registrarse aqui", on_click=mostrar_registro),
                lbl_error
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def mostrar_registro(e):
        page.clean()
        page.add(
            ft.Column([
                ft.Text("Registro Escolar", size=26, weight=ft.FontWeight.BOLD),
                rb_rol, 
                txt_nombre, 
                txt_grupo, 
                txt_reg_usuario, 
                txt_reg_pass,
                ft.ElevatedButton("Registrarse", on_click=registrar_usuario, width=250, bgcolor=ft.Colors.GREEN, color=ft.Colors.WHITE),
                ft.TextButton("Volver al Login", on_click=mostrar_login)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
        page.update()

    def mostrar_pantalla_principal():
        page.clean()
        rol = usuario_logeado["rol"]
        nombre = usuario_logeado["nombre"]
        grupo = usuario_logeado["grupo"]

        if rol == "Alumno":
            def desplegar_caja(e):
                area_reporte.visible = True
                page.update()

            area_reporte = ft.Column([
                txt_incidencia,
                ft.ElevatedButton("Enviar Reporte", on_click=guardar_incidencia, bgcolor=ft.Colors.BLUE_GREY, color=ft.Colors.WHITE)
            ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            btn_rojo = ft.ElevatedButton(
                "BOTON ROJO: SOLICITAR AYUDA", 
                bgcolor=ft.Colors.RED,
                color=ft.Colors.WHITE,
                width=320,
                height=70,
                on_click=desplegar_caja
            )
            page.add(
                ft.Column([
                    ft.Text(f"Alumno: {nombre}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Grupo: {grupo}", size=14),
                    btn_rojo,
                    area_reporte,
                    ft.TextButton("Cerrar Sesion", on_click=mostrar_login)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        else:
            cursor.execute("SELECT alumno, grupo, descripcion FROM incidencias ORDER BY id DESC")
            reportes = cursor.fetchall()
            lista_reportes = ft.ListView(expand=True, spacing=10, max_height=400)
            
            if not reportes:
                lista_reportes.controls.append(ft.Text("No hay incidencias.", italic=True))
            else:
                for rep in reportes:
                    lista_reportes.controls.append(
                        ft.Card(
                            content=ft.Container(
                                content=ft.ListTile(
                                    leading=ft.Icon(ft.Icons.WARNING, color=ft.Colors.RED),
                                    title=ft.Text(f"{rep[0]} - Grupo: {rep[1]}"),
                                    subtitle=ft.Text(f"Problema: {rep[2]}")
                                ), padding=10
                            )
                        )
                    )
            page.add(
                ft.Column([
                    ft.Text(f"Prefecto/Profesor: {nombre}", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text("Lista de Incidencias:"),
                    lista_reportes,
                    ft.TextButton("Cerrar Sesion", on_click=mostrar_login)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            )
        page.update()

    txt_usuario = ft.TextField(label="Usuario", width=300)
    txt_pass = ft.TextField(label="Contrasena", password=True, can_reveal_password=True, width=300)
    lbl_error = ft.Text(color=ft.Colors.RED)
    rb_rol = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="Alumno", label="Alumno"),
        ft.Radio(value="Profesor", label="Profesor")
    ], alignment=ft.MainAxisAlignment.CENTER), value="Alumno", on_change=cambiar_visibilidad_grupo)
    txt_nombre = ft.TextField(label="Nombre Completo", width=300)
    txt_grupo = ft.TextField(label="Grupo", width=300)
    txt_reg_usuario = ft.TextField(label="Nuevo Usuario", width=300)
    txt_reg_pass = ft.TextField(label="Nueva Contrasena", password=True, width=300)
    txt_incidencia = ft.TextField(label="¿Que te esta pasando?", multiline=True, min_lines=3, width=350)

    mostrar_login(None)

if __name__ == "__main__":
    ft.app(target=main)
