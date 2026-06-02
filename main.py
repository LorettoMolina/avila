import flet as ft
from src.views.LoginView import LoginView

def main(page: ft.Page):
    LoginView(page)

ft.app(target=main)