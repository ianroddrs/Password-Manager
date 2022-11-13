import flet
from flet.ref import Ref
from flet import Page,TextField,Row,Text,FilledButton,colors, Container,Column,border_radius, border,ButtonStyle
from flet.buttons import RoundedRectangleBorder, CountinuosRectangleBorder
from modules.functions import init, cadastrar_usuario,login_sistema

def main(page: Page):

    components = {
        'username' : Ref[TextField](),
        'email' : Ref[TextField](),
        'senha' : Ref[TextField](),
        'l_user': Ref[TextField](),
        'l_senha':Ref[TextField]()
        #add todos os compontens da tela aqui
    }

    #passagem das referências para o outro arquivo
    init(components, page)

    page.title = "Cadastro de usuário"
    page.theme_mode = 'light'

    page.window_width = 400
    page.window_min_width = 350
    # page.window_max_width = 400

    page.window_height = 600
    page.window_min_height = 600
    # page.window_max_height = 750
    
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"

    #cadastro de usuário
    titulo = Text(value='Cadastre-se',size=20,weight='bold')
    username = TextField(ref=components['username'],label='Username',bgcolor=colors.BLACK,width=300,height=45,text_size=11,autofocus=True)
    email = TextField(ref=components['email'],label='E-mail', border_color=colors.BLACK,width=300,height=45,text_size=11)
    senha = TextField(ref=components['senha'],label='Senha',border_color=colors.BLACK,width=300,height=45,text_size=11,password=True,can_reveal_password=False)
    botao_cadastrar = FilledButton(text='Cadastre-se',width=300,style=ButtonStyle(shape={"": CountinuosRectangleBorder(radius=20),}),on_click=cadastrar_usuario)

    #login de usuário
    titulo_login = Text(value='Entre',size=20,weight='bold')
    l_username = TextField(ref=components['l_user'],label='Username',bgcolor=colors.BLACK,width=300,height=45,text_size=11,autofocus=False)
    l_senha = TextField(ref=components['l_senha'],label='Senha',border_color=colors.BLACK,width=300,height=45,text_size=11,password=True,can_reveal_password=False)
    botao_login = FilledButton(text='Entrar',width=300,style=ButtonStyle(shape={"": CountinuosRectangleBorder(radius=20),}),on_click=login_sistema)

    page.add(
        Container(
            border= border.all(5, colors.BLACK12),
            border_radius=border_radius.all(20),
            padding=10,
            width= 400,
            
            content=Column(
                horizontal_alignment= "center",
                controls=[
                        titulo,
                        username,
                        email,
                        senha,
                        botao_cadastrar,
                ]
            )
        ),
        Container(
            border= border.all(5, colors.BLACK12),
            border_radius=border_radius.all(20),
            padding=10,
            width= 400,

            content=Column(
                horizontal_alignment= "center",
                controls=[
                    titulo_login,
                    l_username,
                    l_senha,
                    botao_login,
                ]
            )
        ),
        Container(
            bgcolor=colors.BLUE,
            height=50,
            content=Row(

            )
        )

    )

flet.app(target=main)