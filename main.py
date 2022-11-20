from time import sleep
import sqlite3
import flet
from flet import AppBar, Page, Text, View ,ElevatedButton, colors,Container, PopupMenuButton,PopupMenuItem,Row, Icon,icons, NavigationRail,NavigationRailDestination,IconButton,FloatingActionButton,VerticalDivider,Column, ButtonStyle,TextField,FilledButton,margin, TextButton, alignment, AlertDialog
from flet.buttons import RoundedRectangleBorder

def create_DB():
    conexao = sqlite3.connect('usuarios.db')
    c = conexao.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS user_cadastro (
                user_id integer primary key autoincrement,
                username text,
                email text,
                senha text,
                nome text,
                sobrenome text
                )
            ''')
        c.execute
    except:
        pass
    conexao.commit()
    conexao.close()

create_DB()

def main(page: Page):
    page.title = "Password Manager"
    page.theme_mode = "light"
    page.window_min_width = 550
    page.window_min_height = 600

    #ABRIR/FECHAR RAIL
    def open_rail(e):
        rail.visible = True if rail.visible == False else False
        OpenRailMenu.selected = not OpenRailMenu.selected
        sleep(0.2)
        page.update()

    #MUDAR TEMA
    def change_theme(e):
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        sleep(0.2)
        page.update()

    #VERIFICAÇÃO DE EMAIL
    def verificar_email():
        emails_cadastrados = []
        conexao = sqlite3.connect('usuarios.db')
        c = conexao.cursor()
        c.execute("SELECT email from user_cadastro")
        email_bd = c.fetchall()
        for i in email_bd:
            emails_cadastrados.append(i[0])
        conexao.commit()
        conexao.close()
        return emails_cadastrados

    #VERIFICAÇÃO DE USUÁRIO
    def verificar_user():
        users_cadastrados = []
        conexao = sqlite3.connect('usuarios.db')
        c = conexao.cursor()
        c.execute("SELECT username from user_cadastro")
        users_bd = c.fetchall()
        for i in users_bd:
            users_cadastrados.append(i[0])
        conexao.commit()
        conexao.close()
        return users_cadastrados

    #CADASTRAR USUÁRIO
    def cadastrar_usuario(e):
        if username.value in verificar_user() and email.value in verificar_email():
            dlg = AlertDialog(title=Text("username e email ja cadastrado no sistema"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
        elif username.value in verificar_user():
            dlg = AlertDialog(title=Text("username ja cadastrado no sistema"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
        elif email.value in verificar_email():
            dlg = AlertDialog(title=Text("email ja cadastrado no sistema"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()                    
        else:
            conexao = sqlite3.connect('usuarios.db')
            c = conexao.cursor()
            query = "INSERT INTO user_cadastro(nome, sobrenome, username, email, senha) VALUES (?, ?, ?, ?, ?)"
            valores = (nome.value,sobrenome.value,username.value,email.value,senha.value)
            c.execute(query,valores)
            conexao.commit()
            conexao.close()

            username.value = ""
            senha.value = ""
            email.value = ""
            nome.value = ""
            sobrenome.value = ""

            dlg = AlertDialog(title=Text(f"Cadastro realizado com sucesso!"),on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True

            page.update()

    #LOGAR USUÁRIO
    def login_sistema(e):
        '''
            Autenticar Login
        '''
        login = {
            'username': l_username.value,
            'senha': l_senha.value
        }
        conexao = sqlite3.connect('usuarios.db')      
        c = conexao.cursor()
        try:
            c.execute("SELECT senha FROM user_cadastro WHERE username = '{}'".format(login['username']))
            senha_bd = c.fetchall()
            conexao.close()
            l_username.value = ""
            l_senha.value = ""
            page.update
        
            if login['senha'] == senha_bd[0][0]:
                global logado; logado = True
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
        except:
            dlg = AlertDialog(title=Text("Usuario não cadastrado"), on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()

    # Recuperar Senha
    def recuperar_senha(e):    
        if email_cadastrado.value in verificar_email():
                dlg = AlertDialog(title=Text(f"Digite sua nova senha"),content = nova_senha,actions=[
                FilledButton("Alterar senha",on_click=inserir_nova_senha)
            ],on_dismiss=lambda e: print("Dialog dismissed!"))
                page.dialog = dlg
                dlg.open = True
                page.update()
        else:
            dlg = AlertDialog(title=Text("Esse E-mail não pertence a nenhuma conta!"), on_dismiss=lambda e: print("Dialog dismissed!"))
            page.dialog = dlg
            dlg.open = True
            page.update()
    
    # Inserir nova senha no banco de dados
    def inserir_nova_senha(e):
        conexao = sqlite3.connect('usuarios.db')  
        c = conexao.cursor()
        dlg = AlertDialog(title=Text(f"Senha alterada!"),on_dismiss=lambda e: print("Dialog dismissed!"))
        senha_update = """Update user_cadastro set senha = ? where email = ?"""
        valores = (nova_senha.value,email_cadastrado.value)
        c.execute(senha_update,valores)
        conexao.commit()
        conexao.close()
        page.dialog = dlg
        dlg.open = True
        page.update()
    #MENUS

    #MENU LOGIN USUÁRIO
    titulo_login = Text(value='Entre',weight='bold',size=30)
    l_username = TextField(label='Username',autofocus=True,expand=False,prefix_icon=icons.ACCOUNT_CIRCLE,width=500)
    l_senha = TextField(label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500)
    esqueceu_senha = TextButton(text="Redefinir senha",on_click= lambda _: page.go("/recuperar"), style=ButtonStyle(color={"hovered": colors.BLUE_900,},bgcolor={"hovered": colors.TRANSPARENT, "": colors.TRANSPARENT},))
    botao_login = FilledButton(text='Entrar',on_click=login_sistema,width=500,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)},))
    botao_pagina_cadastrar = TextButton(text="CADASTRAR",on_click= lambda _: page.go("/cadastro"), style=ButtonStyle(color={"hovered": colors.BLUE_900,},))
    global logado; logado = False

    #MENU CADASTRO USUÁRIO
    titulo = Text(value='Cadastre-se',weight='bold',size=30)
    nome = TextField(label='Nome',autofocus=True,prefix_icon=icons.PERSON,width=245)
    sobrenome = TextField(label='Sobrenome',prefix_icon=icons.PERSON,width=245)
    username = TextField(label='Username',prefix_icon=icons.ACCOUNT_CIRCLE,width=500)
    email = TextField(label='E-mail', border_color=colors.BLACK,prefix_icon=icons.EMAIL,width=500)
    senha = TextField(label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500)
    botao_cadastrar = FilledButton(text='Cadastrar',width=500,on_click=cadastrar_usuario,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)},))
    botao_pagina_login = TextButton(text="FAÇA LOGIN",on_click= lambda _: page.go("/"), style=ButtonStyle(color={"hovered": colors.BLUE_900,},))

    #MENU APPBAR
    OpenRailMenu = IconButton(icon=icons.MENU_OUTLINED, selected_icon=icons.MENU_OPEN, on_click=open_rail)
    theme_icon_button = IconButton(icons.DARK_MODE, selected_icon=icons.LIGHT_MODE, icon_color=colors.BLACK,icon_size=25, tooltip="change theme", on_click=change_theme,style=ButtonStyle(color={"": colors.BLACK, "selected": colors.WHITE}, ), )
    textAppBar = ""; AppBarMenu =AppBar(leading_width=110,title=Text(textAppBar), bgcolor=colors.SURFACE_VARIANT,actions=[theme_icon_button,PopupMenuButton(items=[PopupMenuItem()])])

    #MENU RECUPERAR SENHA
    titulo_recuperar_senha = Text(value='Recupere sua Senha',weight='bold',size=30)
    email_cadastrado= TextField(label='E-mail Cadastrado', border_color=colors.BLACK,prefix_icon=icons.EMAIL,width=500)
    botao_verificar_email  = FilledButton(text='VERIFICAR',on_click=recuperar_senha,width=500,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)},))
    nova_senha = TextField(label='Nova Senha',border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500)
    
    #LOGOUT DE SISTEMA
    def logout(e):
        page.go("/")
        global logado; logado = False

    #BOTÃO DE SAIR
    btn_logout = Container(content=ElevatedButton(color=colors.WHITE,bgcolor=colors.RED,icon=icons.ARROW_LEFT,text='SAIR',width=100,height=50,on_click=logout,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)})),margin=margin.only(top=50))

    
    # RAIL NAVIGATION
    pages = [
        Text("PERFIL", visible=False),
        Container(
            expand=True,bgcolor=colors.AMBER,
            content=Row(
                [
                    Container(scale=0.5,expand=True,bgcolor=colors.BLUE),
                    Container(expand=True,bgcolor=colors.RED,),
                ]
            )


        ),
        Text("SETTINGS", visible=False),
    ]

    def fab_click(e):
        rail.selected_index = 2
        select_page()
        page.update()

    def select_page():
        print(f"Selected index: {rail.selected_index}")
        for index, p in enumerate(pages):
            p.visible = True if index == rail.selected_index else False

        if rail.selected_index == 0:
            AppBarMenu.title = Text("Perfil")
        elif rail.selected_index == 1:
            AppBarMenu.title = Text("Senhas")
        elif rail.selected_index == 2:
            AppBarMenu.title = Text("Settings")
        page.update()

    def dest_change(e):
        select_page()


    rail = NavigationRail(
        visible=False,
        selected_index=1,
        label_type="all",
        extended=False,
        min_width=90,
        leading=Container(content=FloatingActionButton(icon=icons.ADD,width=100, text="GERAR",on_click=fab_click),margin=margin.only(bottom=15)),
        group_alignment=-1,
        trailing = btn_logout,
        destinations=[
            NavigationRailDestination(
                icon=icons.ACCOUNT_CIRCLE, label="PERFIL"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.KEY),label="SENHAS",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS_OUTLINED, label_content=Text("SETTINGS"),
            ),
        ],
        on_change=dest_change,
    )

    #ROTAS 

    def route_change(route):
        AppBarMenu.title = Text("Login")
        AppBarMenu.leading = None
        page.views.clear()
        page.views.append(
            View(
                "/",
                [
                    AppBarMenu,
                    Container(content=Row(
                        [
                            Column(controls=[
                                    Container(content=titulo_login,width=500,alignment=alignment.center_left,margin=margin.only(bottom=15)),
                                    l_username,l_senha, 
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
        if page.route == "/cadastro":
            AppBarMenu.title = Text("Cadastro")
            AppBarMenu.leading = None
            page.views.append(
                View(
                    "/cadastro",
                    [
                        AppBarMenu,
                        Container(content=Row(
                            [
                                Column(controls=[
                                        Container(content=titulo,width=500,alignment=alignment.center_left,margin=margin.only(bottom=15)),
                                        Row([nome,sobrenome,],alignment="center"),username,email,senha,botao_cadastrar,
                                        Container(width=500, bgcolor=colors.BLACK45,height=1,margin=20),
                                        Text("Já é cadastrado?"),botao_pagina_login,
                                    ],scroll="hidden",expand=True,alignment="center",horizontal_alignment="center"
                                )
                            ],expand=True,
                        ),expand=True),
                       
                    ],
                )
            )
        elif page.route == "/recuperar":
            AppBarMenu.title = Text("Recuperação de Senha")
            AppBarMenu.leading = None
            page.views.append(
                View(
                    "/recuperar",
                    [
                        AppBarMenu,
                        Container(content=Row(
                            [
                                Column(controls=[
                                        Container(content=titulo_recuperar_senha,width=500,alignment=alignment.center_left,margin=margin.only(bottom=15)),
                                        Row([email_cadastrado],alignment="center"),botao_verificar_email
                                    ],expand=True,alignment="center",horizontal_alignment="center"
                                )
                            ],expand=True,
                        ),expand=True),
                       
                    ],
                )
            )          
        elif page.route == "/Perfil":
            if logado:
                AppBarMenu.title = Text("Senhas")
                AppBarMenu.leading = OpenRailMenu
                page.views.append(
                    View(
                        "/Perfil",
                        [
                            AppBarMenu,
                            Row([rail,VerticalDivider(width=1),Column(pages,expand=True)],expand=True)
                        
                        ],
                    )
                )
            else: 
                page.views.append(
                    View(
                        "/Perfil",
                        [
                            Container(content=Row(
                            [
                                Column(controls=[
                                        Text("Nenhum usuário logado!"),botao_pagina_login,
                                    ],expand=True,alignment="center",horizontal_alignment="center"
                                ), 
                            ],expand=True,
                            ),expand=True
                            )
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