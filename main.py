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
    # Configuración estética global de la ventana
    page.title = "Sistema de Incidencias"
    page.window_width = 450
    page.window_height = 730
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#14171A"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def iniciar_sesion(e):
        global usuario_logeado
        cursor.execute("SELECT rol, nombre, grupo FROM usuarios WHERE usuario=? AND contrasena=?", 
                       (txt_usuario.value, txt_pass.value))
        usuario = cursor.fetchone()
        if usuario:
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
            mostrar_alerta("Éxito", "Registrado correctamente.")
            mostrar_login(None)
        except sqlite3.IntegrityError:
            mostrar_alerta("Error", "El usuario ya existe.")

    def guardar_incidencia(e):
        if not txt_incidencia.value:
            mostrar_alerta("Aviso", "Escribe una descripción.")
            return
        cursor.execute("INSERT INTO incidencias (alumno, grupo, descripcion) VALUES (?, ?, ?)",
                       (usuario_logeado["nombre"], usuario_logeado["grupo"], txt_incidencia.value))
        conn.commit()
        mostrar_alerta("Enviado", "Incidencia registrada.")
        txt_incidencia.value = ""
        mostrar_pantalla_principal()

    def eliminar_incidencia(id_incidencia):
        cursor.execute("DELETE FROM incidencias WHERE id=?", (id_incidencia,))
        conn.commit()
        mostrar_alerta("Completado", "La incidencia ha sido eliminada.")
        mostrar_pantalla_principal()

    def cambiar_visibilidad_grupo(e):
        txt_grupo.visible = True if rb_rol.value == "Alumno" else False
        page.update()

    def mostrar_alerta(titulo, mensaje):
        def cerrar_dialogo(e):
            dlg.open = False
            page.update()
        dlg = ft.AlertDialog(
            title=ft.Text(titulo, weight=ft.FontWeight.BOLD),
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
        
        login_card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.LOCK_PERSON_ROUNDED, size=50, color=ft.Colors.BLUE_400),
                ft.Text("Inicio de Sesión", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Ingresa tus credenciales", size=12, color=ft.Colors.GREY_500),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                txt_usuario, 
                txt_pass,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.ElevatedButton(
                    "Entrar", 
                    on_click=iniciar_sesion, 
                    width=300, 
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    bgcolor=ft.Colors.BLUE_600, 
                    color=ft.Colors.WHITE
                ),
                ft.TextButton("¿No tienes cuenta? Regístrate aquí", on_click=mostrar_registro, style=ft.ButtonStyle(color=ft.Colors.BLUE_400)),
                lbl_error
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1E2229",
            padding=30,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=10, color="#000000")
        )
        
        page.add(login_card)
        page.update()

    def mostrar_registro(e):
        page.clean()
        
        registro_card = ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.SCHOOL_ROUNDED, size=50, color=ft.Colors.GREEN_400),
                ft.Text("Registro Escolar", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                rb_rol, 
                txt_nombre, 
                txt_grupo, 
                txt_reg_usuario, 
                txt_reg_pass,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.ElevatedButton(
                    "Registrarse", 
                    on_click=registrar_usuario, 
                    width=300, 
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    bgcolor=ft.Colors.GREEN_600, 
                    color=ft.Colors.WHITE
                ),
                ft.TextButton("Volver al Login", on_click=mostrar_login, style=ft.ButtonStyle(color=ft.Colors.GREY_400))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#1E2229",
            padding=25,
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=10, color="#000000")
        )
        
        page.add(registro_card)
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
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                txt_incidencia,
                ft.ElevatedButton(
                    "Enviar Reporte Oficial", 
                    on_click=guardar_incidencia, 
                    width=320,
                    height=45,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8)),
                    bgcolor=ft.Colors.BLUE_GREY_700, 
                    color=ft.Colors.WHITE
                )
            ], visible=False, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            btn_rojo = ft.Container(
                content=ft.ElevatedButton(
                    "🚨 BOTÓN ROJO: SOLICITAR AYUDA", 
                    bgcolor=ft.Colors.RED_600,
                    color=ft.Colors.WHITE,
                    width=320,
                    height=75,
                    on_click=desplegar_caja,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=12),
                        text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD)
                    )
                ),
                shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.RED_900)
            )
            
            alumno_card = ft.Container(
                content=ft.Column([
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=40, color=ft.Colors.BLUE_400),
                        title=ft.Text(f"{nombre}", size=18, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Text(f"Grupo: {grupo}", size=13, color=ft.Colors.GREY_400)
                    ),
                    ft.Divider(color=ft.Colors.GREY_800),
                    ft.Divider(height=15, color=ft.Colors.TRANSPARENT),
                    btn_rojo,
                    area_reporte,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    ft.TextButton("Cerrar Sesión", on_click=mostrar_login, style=ft.ButtonStyle(color=ft.Colors.RED_300))
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor="#1E2229",
                padding=20,
                border_radius=15,
                width=380
            )
            page.add(alumno_card)
            
        else:
            cursor.execute("SELECT id, alumno, grupo, descripcion FROM incidencias ORDER BY id DESC")
            reportes = cursor.fetchall()
            lista_reportes = ft.ListView(expand=True, spacing=12, height=420)

            if not reportes:
                lista_reportes.controls.append(
                    ft.Container(
content=ft.Text("No hay incidencias activas en este momento.", 
                italic=True, color=ft.Colors.GREY_500, text_align=ft.TextAlign.CENTER),padding=20,alignment=ft.alignment.center))else:for rep in reportes:id_actual = rep[0]lista_reportes.controls.append(ft.Card(color="#252A34",elevation=4,content=ft.Container(content=ft.ListTile(leading=ft.Icon(ft.Icons.REPORT_PROBLEM_ROUNDED, color=ft.Colors.AMBER_400, size=30),title=ft.Text(f"{rep[1]}", weight=ft.FontWeight.BOLD, size=15),subtitle=ft.Column([ft.Text(f"Grupo: {rep[2]}", size=12, color=ft.Colors.BLUE_200, weight=ft.FontWeight.W_500),ft.Text(f"{rep[3]}", size=13, color=ft.Colors.GREY_300)], spacing=3),trailing=ft.IconButton(icon=ft.Icons.CHECK_CIRCLE_ROUNDED,icon_color=ft.Colors.GREEN_400,icon_size=28,tooltip="Marcar como resuelto",on_click=lambda e, idx=id_actual: eliminar_incidencia(idx))), padding=12)))profe_card = ft.Container(content=ft.Column([ft.ListTile(leading=ft.Icon(ft.Icons.SUPERVISOR_ACCOUNT_ROUNDED, size=40, color=ft.Colors.GREEN_400),title=ft.Text(f"Prof: {nombre}", size=18, weight=ft.FontWeight.BOLD),subtitle=ft.Text("Panel de Control Escolar", size=12, color=ft.Colors.GREY_400)),ft.Divider(color=ft.Colors.GREY_800),ft.Text("Alertas Recientes:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_300),lista_reportes,ft.Divider(height=10, color=ft.Colors.TRANSPARENT),ft.TextButton("Cerrar Sesión", on_click=mostrar_login, style=ft.ButtonStyle(color=ft.Colors.RED_300))]),bgcolor="#1E2229",padding=20,border_radius=15,width=400)page.add(profe_card)page.update()txt_usuario = ft.TextField(label="Usuario", width=300, prefix_icon=ft.Icons.PERSON, border_radius=8, bgcolor="#14171A")txt_pass = ft.TextField(label="Contraseña", password=True, can_reveal_password=True, width=300, prefix_icon=ft.Icons.KEY, border_radius=8, bgcolor="#14171A")lbl_error = ft.Text(color=ft.Colors.RED_400, weight=ft.FontWeight.BOLD, size=13)rb_rol = ft.RadioGroup(content=ft.Row([ft.Radio(value="Alumno", label="Alumno"),ft.Radio(value="Profesor", label="Profesor")], alignment=ft.MainAxisAlignment.CENTER), value="Alumno", on_change=cambiar_visibilidad_grupo)txt_nombre = ft.TextField(label="Nombre Completo", width=300, prefix_icon=ft.Icons.BADGE, border_radius=8, bgcolor="#14171A")txt_grupo = ft.TextField(label="Grupo", width=300, prefix_icon=ft.Icons.GROUP, border_radius=8, bgcolor="#14171A")txt_reg_usuario = ft.TextField(label="Nuevo Usuario", width=300, prefix_icon=ft.Icons.PERSON_ADD, border_radius=8, bgcolor="#14171A")txt_reg_pass = ft.TextField(label="Nueva Contraseña", password=True, width=300, prefix_icon=ft.Icons.PASSWORD, border_radius=8, bgcolor="#14171A")txt_incidencia = ft.TextField(label="¿Qué emergencia o situación ocurre?",multiline=True,min_lines=3,width=320,border_radius=8,bgcolor="#14171A")mostrar_login(None)if name == "main":ft.app(target=main) 