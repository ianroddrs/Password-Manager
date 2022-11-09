import sqlite3
import flet
from flet import page,TextField,Container,Row,Text,FilledButton,colors,alignment,theme, Container
from functions.cadastro import cadastrar_usuario


def main(page):
    page.title = "Cadastro"
    page.theme_mode = 'light'
    page.window_width = 350
    page.window_height = 700
    page.horizontal_alignment = 'end'
    

    titulo = Text(value='Cadastre-se',size=20,weight='bold')
    
    username = TextField(label='Username',bgcolor=colors.BLACK,autofocus=True)
    
    email = TextField(label='E-mail', border_color=colors.BLACK)
    
    senha = TextField(label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=False)

    botao_cadastrar = FilledButton(text='Cadastrar',on_click=cadastrar_usuario)
    
    page.add(
	Row([titulo]),
        Row([username],alignment="center"),
	Row([email],alignment="center"),
	Row([senha],alignment="center"),
        Row([botao_cadastrar],alignment="center")
    )

flet.app(target=main)