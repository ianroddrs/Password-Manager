import flet
from flet.ref import Ref
from flet import Page,TextField,Row,Text,FilledButton,colors
from functions.cadastro import init, cadastrar_usuario

def main(page: Page):

    components = {
        'username' : Ref[TextField](),
        'email' : Ref[TextField](),
        'senha' : Ref[TextField](),
        #add todos os compontens da tela aqui
    }

    #passagem das referências para o outro arquivo
    init(components, page)

    page.title = "Cadastro"
    page.theme_mode = 'light'
    page.window_width = 400
    page.window_height = 700

    titulo = Text(value='Cadastre-se',size=20,weight='bold')
    
    username = TextField(ref=components['username'],label='Username',bgcolor=colors.BLACK,autofocus=True)
    
    email = TextField(ref=components['email'],label='E-mail', border_color=colors.BLACK)
    
    senha = TextField(ref=components['senha'],label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=False)

    botao_cadastrar = FilledButton(text='Cadastre-se',on_click=cadastrar_usuario)

    page.add(
        Row(
            [titulo]
        ),
        Row(
            [username],
            alignment="center"
        ),
        Row(
            [email],
            alignment="center"
        ),
        Row(
            [senha],
            alignment="center"
        ),
        Row(
            [botao_cadastrar],
            alignment="center"
        )
    )

flet.app(target=main)