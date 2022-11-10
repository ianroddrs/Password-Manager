import sqlite3
import flet
from flet import page,TextField,Container,Row,Text,FilledButton,colors,alignment,theme

"""
 Criação banco de dados
 conexao = sqlite3.connect('usuarios.db')
 c = conexao.cursor()
 c.execute('''CREATE TABLE user_cadastro (
         username text,
         email text,
         senha text
         )
     ''')
 conexao.commit()
 conexao.close()
"""


def main(page):
    page.title = "Cadastro"
    page.theme_mode = 'light'
    page.window_width = 400
    page.window_height = 700
    #page.horizontal_alignment = 'center'

    def cadastrar_usuario(e):
        cadastro = {
            'username': username.value,
            'email': email.value,
            'senha': senha.value
        }
        conexao = sqlite3.connect('usuarios.db')
        
        c = conexao.cursor()

        c.execute(" INSERT INTO user_cadastro VALUES(:username, :email, :senha)",
            {
                'username':cadastro['username'],
                'email':cadastro['email'],
                'senha':cadastro['senha'] 
            }
        )
        conexao.commit()
        conexao.close()
    

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