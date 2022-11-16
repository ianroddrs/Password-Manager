from time import sleep
import sqlite3
import flet
from flet import AppBar, ElevatedButton, Page, Text, View, colors, Container, PopupMenuButton,PopupMenuItem,Row, Icon,icons, NavigationRail,NavigationRailDestination,IconButton,FloatingActionButton,VerticalDivider,Column, ButtonStyle,TextField,FilledButton, TextButton, alignment
from flet.buttons import RoundedRectangleBorder
from modules.functions import create_DB

create_DB()

def main(page: Page):
    page.title = "Password Manager"
    page.theme_mode = "light"

    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        sleep(0.2)
        page.update()

    def cadastrar_usuario(e):
        cadastro = {
            'username': username.value,
            'email':  email.value,
            'senha':  senha.value
        }

        username.value = ""
        senha.value = ""
        email.value = ""
        page.update

        conexao = sqlite3.connect('Password-Manager/usuarios.db')
    
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

    def login_sistema(e):
        from flet import AlertDialog, Text
        '''
            Autenticar Login
        '''
        login = {
            'username': l_username.value,
            'senha': l_senha.value
        }
        conexao = sqlite3.connect('Password-Manager/usuarios.db')      
        
        c = conexao.cursor()
        c.execute("SELECT senha FROM user_cadastro WHERE username = '{}'".format(login['username']))
        senha_bd = c.fetchall()
        conexao.close()

        l_username.value = ""
        l_senha.value = ""
        page.update
        
        if login['senha'] == senha_bd[0][0]:
            dlg = AlertDialog(title=Text(f"Hello {login['username']}!"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.go("/Perfil")
            page.update()
        else:
            dlg = AlertDialog(title=Text("Senha Incorreta!"), on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()

    #login de usuário
    titulo_login = Text(value='Entre',weight='bold')
    l_username = TextField(label='Username',autofocus=True,expand=False,prefix_icon=icons.ACCOUNT_CIRCLE,width=500)
    l_senha = TextField(label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500)
    esqueceu_senha = TextButton(text="Redefinir senha",on_click= lambda _: print(""), style=ButtonStyle(
                color={
                    "hovered": colors.BLUE_900,
                },
                bgcolor={"hovered": colors.TRANSPARENT, "": colors.TRANSPARENT},))
    botao_login = FilledButton(text='Entrar',on_click=login_sistema,width=500,style=ButtonStyle(shape={
                    "hovered": RoundedRectangleBorder(radius=20),
                    "": RoundedRectangleBorder(radius=5)},))
    botao_pagina_cadastrar = TextButton(text="CADASTRAR",on_click= lambda _: page.go("/cadastro"), style=ButtonStyle(
                color={
                    "hovered": colors.BLUE_900,
                },))


    #cadastro de usuário
    titulo = Text(value='Cadastre-se',weight='bold')
    username = TextField(label='Username',autofocus=True,prefix_icon=icons.ACCOUNT_CIRCLE,width=500)
    email = TextField(label='E-mail', border_color=colors.BLACK,prefix_icon=icons.EMAIL,width=500)
    senha = TextField(label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500)
    botao_cadastrar = FilledButton(text='Cadastrar',width=500,on_click=cadastrar_usuario,style=ButtonStyle(shape={
                    "hovered": RoundedRectangleBorder(radius=20),
                    "": RoundedRectangleBorder(radius=5)},))
    botao_pagina_login = TextButton(text="FAÇA LOGIN",on_click= lambda _: page.go("/"), style=ButtonStyle(
                color={
                    "hovered": colors.BLUE_900,
                },))



    rail = NavigationRail(
        selected_index=0,
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.CREATE, text="Add"),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.FAVORITE_BORDER, selected_icon=icons.FAVORITE, label="First"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.BOOKMARK_BORDER),
                selected_icon_content=Icon(icons.BOOKMARK),
                label="Second",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED,
                selected_icon_content=Icon(icons.SETTINGS),
                label_content=Text("Settings"),
            ),
        ],
        on_change=lambda e: print("Selected destination:", e.control.selected_index),
    )

    theme_icon_button = IconButton(icons.DARK_MODE, selected_icon=icons.LIGHT_MODE, icon_color=colors.BLACK,
                                   icon_size=25, tooltip="change theme", on_click=change_theme,
                                   style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}, ), )

    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBar(title=Text("Login"), bgcolor=colors.SURFACE_VARIANT,actions=[
                        theme_icon_button,
                        PopupMenuButton(
                            items=[
                                PopupMenuItem()
                            ]
                        )
                    ]),
                    Container(content=Row(
                        [
                            Column(controls=[
                                    titulo_login,l_username,l_senha, 
                                    Container(content=esqueceu_senha,width=500,alignment=alignment.center_left),
                                    botao_login,
                                    Container(width=500, bgcolor=colors.BLACK45,height=1,margin=20),
                                    Text("Não tem conta?"),botao_pagina_cadastrar,
                                ],expand=True,alignment="center",horizontal_alignment="center"
                            )
                        ],expand=True,
                    ),expand=True),
                    
                    
                ]
            )
        )
        if page.route == "/Perfil":
            page.views.append(
                View(
                    "/Perfil",
                    [
                        AppBar(title=Text("Perfil"), bgcolor=colors.SURFACE_VARIANT, leading=IconButton(icons.PUBLIC_OFF)),
                        Row([rail,VerticalDivider(width=1), ElevatedButton("Sair", on_click=lambda _: page.go("/")),],expand=True)
                       
                    ],
                )
            )
        elif page.route == "/cadastro":
            page.views.append(
                View(
                    "/cadastro",
                    [
                        AppBar(title=Text("Cadastro"), bgcolor=colors.SURFACE_VARIANT,actions=[
                        theme_icon_button,
                        PopupMenuButton(
                            items=[
                                PopupMenuItem()
                            ]
                        )
                    ]),
                        Container(content=Row(
                            [
                                Column(controls=[
                                        titulo,username,email,senha,botao_cadastrar,
                                        Container(width=500, bgcolor=colors.BLACK45,height=1,margin=20),
                                        Text("Já é cadastrado?"),botao_pagina_login,
                                    ],expand=True,alignment="center",horizontal_alignment="center"
                                )
                            ],expand=True,
                        ),expand=True),
                       
                    ],
                )
            )

        page.update()
    

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)



flet.app(target=main) #view=flet.WEB_BROWSER