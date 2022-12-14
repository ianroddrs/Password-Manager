from time import sleep
import sqlite3
import flet
from flet import AppBar, Page, Text, View ,ElevatedButton,SnackBar,Stack,ListTile, colors,Divider,Container, PopupMenuButton,PopupMenuItem,Row, Icon,icons, NavigationRail,NavigationRailDestination,IconButton,FloatingActionButton,VerticalDivider,Column, ButtonStyle,TextField,FilledButton,margin, TextButton, alignment, AlertDialog
from flet.buttons import RoundedRectangleBorder
from Crypto.Cipher import AES
from base64 import b64encode
from secrets import token_bytes
import pyperclip as pc 

def create_DB():
    conexao = sqlite3.connect('usuarios.db')
    c = conexao.cursor()
    try:
        c.execute('''CREATE TABLE IF NOT EXISTS user_cadastro (
                user_id integer primary key autoincrement,
                username text NOT NULL,
                email text NOT NULL,
                senha text NOT NULL,
                nome text NOT NULL,
                sobrenome text NOT NULL
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
    page.window_min_width = 600
    page.window_min_height = 600
    page.horizontal_alignment = "center"
    page.window_always_on_top = True

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
    
    # VALIDAR EMAIL
    def validar_email(email):  
        import re
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if(re.search(regex,email)):  
            return("Valid Email")     
        else:  
            return("Invalid Email")
    
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
        if username.value == '' or email.value == '' or nome.value == '' or senha.value == '' or sobrenome.value == '':
            page.snack_bar = SnackBar(Text("Nenhum campo pode estar em branco!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
        elif username.value in verificar_user() and email.value in verificar_email():
            page.snack_bar = SnackBar(Text("Username e E-mail já cadastrados no sistema!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
        elif username.value in verificar_user():
            page.snack_bar = SnackBar(Text("Username já cadastrado no sistema!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
        elif email.value in verificar_email():
            page.snack_bar = SnackBar(Text("E-mail já cadastrado no sistema!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
        elif validar_email(email.value) == "Invalid Email":
            page.snack_bar = SnackBar(Text("E-mail em formato inválido!",size=20),bgcolor=colors.RED,open=True)
            
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

            page.snack_bar = SnackBar(Text("Cadastro realizado com sucesso!",size=20),bgcolor=colors.GREEN,open=True)
            

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
        if l_username.value == '' or l_senha.value == '':
            page.snack_bar = SnackBar(Text("Nenhum campo pode estar em branco!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
        else:
            try:
                c.execute("SELECT senha FROM user_cadastro WHERE username = '{}'".format(login['username']))
                senha_bd = c.fetchall()
                c.execute("SELECT user_id FROM user_cadastro WHERE username = '{}'".format(login['username']))
                global user_logado
                user_logado = c.fetchall()[0][0]

                c.execute(f'''CREATE TABLE IF NOT EXISTS user_senhas{user_logado} (
                    senha_id integer primary key autoincrement,
                    nome text NOT NULL,
                    desc text NOT NULL,
                    senha text NOT NULL
                    )
                ''')
                c.execute

                conexao.close()
            
                if login['senha'] == senha_bd[0][0]:
                    global logado; logado = True
                    dlg = AlertDialog(title=Text(f"Seja bem-vindo, {login['username']}!"),on_dismiss=lambda e: print("Dialog dismissed!"))
                    page.dialog = dlg
                    dlg.open = True
                    l_username.value = ""
                    l_senha.value = ""
                    page.update
                    page.go("/Perfil")
                    atualizar_lista_senhas()
                    page.update()
                else:
                    page.snack_bar = SnackBar(Text("Senha incorreta!",size=20),bgcolor=colors.RED,open=True)
                    
                    page.update()
            except:
                page.snack_bar = SnackBar(Text("Usuário não cadastrado!",size=20),bgcolor=colors.RED,open=True)
                
                page.update()

    # redefinir Senha
    def redefinir_senha(e):    
        if email_cadastrado.value == '':
            page.snack_bar = SnackBar(Text("Nenhum campo pode estar em branco!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
        elif email_cadastrado.value in verificar_email():
            page.snack_bar = SnackBar(Text("E-mail Encontrado!",size=20),bgcolor=colors.GREEN,open=True)
            
            email_cadastrado.visible = False
            botao_verificar_email.visible = False
            nova_senha.visible = True
            botao_alterar_senha.visible = True
            page.update()
        else:
            page.snack_bar = SnackBar(Text("E-mail não pertence a nenhuma conta cadastrada!",size=20),bgcolor=colors.RED,open=True)
            
            page.update()
    
    # Inserir nova senha no banco de dados
    def inserir_nova_senha(e):
        conexao = sqlite3.connect('usuarios.db')  
        c = conexao.cursor()
        page.snack_bar = SnackBar(Text("Senha redefinida com sucesso!",size=20),bgcolor=colors.GREEN,open=True)
        
        senha_update = """Update user_cadastro set senha = ? where email = ?"""
        valores = (nova_senha.value,email_cadastrado.value)
        c.execute(senha_update,valores)
        conexao.commit()
        conexao.close()
        email_cadastrado.visible = True
        botao_verificar_email.visible = True
        nova_senha.visible = False
        botao_alterar_senha.visible = False
        nova_senha.value = ""
        email_cadastrado.value = ""
        page.go("/")
        page.update()

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

    #LOGOUT DE SISTEMA
    def logout(e):
        page.go("/")
        global logado; logado = False

    #IR PARA RAIL SELECIONADO
    def fab_click(e):
        rail.selected_index = 2
        select_page()
        page.update()

    #MENU PARA GERAR SENHAS
    def menu_add_senhas(e):
        page.dialog = dlg_gerar_senha
        dlg_gerar_senha.open = True
        page.update()

    def add_senhas(e):
        senha_encript = encrypt(nome_sistema.value+descricao_sistema.value+str(user_logado))
        conexao = sqlite3.connect('usuarios.db')      
        c = conexao.cursor()
        query = f"""INSERT INTO user_senhas{user_logado}(nome, desc, senha) VALUES (?, ?, ?)"""
        valores = (nome_sistema.value,descricao_sistema.value,senha_encript)
        c.execute(query,valores)
        conexao.commit()
        conexao.close()
        atualizar_lista_senhas()
        nome_sistema.value = ""
        descricao_sistema.value= ""
        dlg_gerar_senha.open = False
        page.update()

    def close_dlg(e):
        dlg_gerar_senha.open = False
        page.update()

    def encrypt(mensagem, key = token_bytes(16)):
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext = cipher.encrypt(mensagem.encode())
        ciphertext = b64encode(ciphertext).decode()
        return ciphertext
    

    #VERIFICAÇÃO DADOS GERADOS PELO USUÁRIO
    def verificar_dados_user():
        dados_cadastrados = []
        conexao = sqlite3.connect('usuarios.db')
        c = conexao.cursor()
        c.execute(f"""SELECT nome from user_senhas{user_logado}""")
        nomes_geradas = c.fetchall()
        c.execute(f"""SELECT desc from user_senhas{user_logado}""")
        desc_gerados = c.fetchall()
        c.execute(f"""SELECT senha from user_senhas{user_logado}""")
        senhas_geradas = c.fetchall()
        for i in zip(nomes_geradas,desc_gerados,senhas_geradas):
            dados_cadastrados.append(i)
        conexao.commit()
        conexao.close()
        return dados_cadastrados

    

    def atualizar_lista_senhas():
        dados = verificar_dados_user()
        lista_senhas.controls.clear()
        for i in range(len(dados)):
            senha =dados[i][2][0]
            item_senha = ListTile(
                                leading=Icon(icons.KEY),
                                title=Text(dados[i][0][0],width=100),
                                subtitle=Text(dados[i][1][0],width=100),
                                trailing=Row([Stack([
                                        Text(senha[:9]+"...",left=0,width=200),
                                        IconButton(icon=icons.COPY,left=120,on_click=copiar),
                                        IconButton(icon=icons.EDIT,right=50),
                                        IconButton(icon=icons.DELETE,right=0)
                                    ],width=400)
                                    
                                ],width=500,alignment="center")
            )
            
            lista_senhas.controls.append(item_senha)

        page.update()

    def copiar(e):
        pc.copy()
        page.snack_bar = SnackBar(Text("Copiado para área de transferência!"))
        page.snack_bar.open = True
        page.update()

    

    #MENUS

    #MENU LOGIN USUÁRIO
    titulo_login = Text(value='Entre',weight='bold',size=30)
    l_username = TextField(label='Username',autofocus=True,expand=False,prefix_icon=icons.ACCOUNT_CIRCLE,width=500)
    l_senha = TextField(label='Senha',border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500)
    esqueceu_senha = TextButton(text="Redefinir senha",on_click= lambda _: page.go("/redefinir"), style=ButtonStyle(color={"hovered": colors.BLUE_900,},bgcolor={"hovered": colors.TRANSPARENT, "": colors.TRANSPARENT},))
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

    #MENU redefinir SENHA
    titulo_redefinir_senha = Text(value='Redefina sua Senha',weight='bold',size=30)
    email_cadastrado= TextField(label='E-mail Cadastrado', border_color=colors.BLACK,prefix_icon=icons.EMAIL,width=500,scale=0.9)
    botao_verificar_email = IconButton(icon=icons.SEARCH,bgcolor=colors.BLUE_800,icon_color=colors.WHITE,scale=1.5,on_click=redefinir_senha,style=ButtonStyle(bgcolor={"hovered":colors.BLUE_900},shape={"hovered": RoundedRectangleBorder(radius=13)}))
    nova_senha = TextField(label='Nova Senha',helper_text="Digite sua nova senha",border_color=colors.BLACK,password=True,can_reveal_password=True,prefix_icon=icons.PASSWORD,width=500,visible=False)
    botao_alterar_senha = FilledButton(text='Alterar Senha',width=500,on_click=inserir_nova_senha,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)},),visible=False)

    #RAIL NAVIGATION
    #BOTÕES GERAR E SAIR
    btn_logout = Container(content=ElevatedButton(color=colors.WHITE,bgcolor=colors.RED,icon=icons.ARROW_LEFT,text='SAIR',width=100,height=50,on_click=logout,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)})),margin=margin.only(top=50))
    btn_gerar = Container(content=FloatingActionButton(icon=icons.ADD,width=100, text="GERAR",on_click=menu_add_senhas),margin=margin.only(bottom=15))

    #MENU GERAR SENHA
    nome_sistema = TextField(label="Nome do sistema",prefix_icon=icons.INFO)
    descricao_sistema= TextField(label="Descrição",prefix_icon=icons.INFO)
    botao_gerar_senha= FilledButton(text='Gerar Senha',width=500,on_click=add_senhas,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)},))
    dlg_gerar_senha = AlertDialog(title=Text("Cadastre uma nova senha"), on_dismiss=lambda e: print("Dialog dismissed!"),open = True,content=Row([nome_sistema,descricao_sistema,botao_gerar_senha],wrap=True),modal=True,actions=[
            TextButton("Fechar", on_click=close_dlg),
        ],
        actions_alignment="center",)

    
    lista_senhas = Column([
        
    ],scroll="hidden",width=1200,expand=True)

    #EDIÇÃO DE USUÁRIO
    edit_nome = TextField(label='Nome',autofocus=True,prefix_icon=icons.PERSON,width=245)
    edit_sobrenome = TextField(label='Sobrenome',prefix_icon=icons.PERSON,width=245)
    edit_username = TextField(label='Username',prefix_icon=icons.ACCOUNT_CIRCLE,width=500)
    edit_email = TextField(label='E-mail', border_color=colors.BLACK,prefix_icon=icons.EMAIL,width=500)
    user_Edit= [
        Column(controls=[
                Row([edit_nome,edit_sobrenome,],alignment="center"),edit_username,edit_email,botao_cadastrar,
                Container(width=500, bgcolor=colors.BLACK45,height=1,margin=20),
            ],scroll="hidden",expand=True,alignment="center",horizontal_alignment="center"
        )
    ]

    
    
    #PAGINAS
    pages = [
        Container(content=Row(
                        [
                            Column(controls=[
                                    Row([Text(value="EDIÇÃO DE DADOS",size=50)], alignment="center"),
                                    Divider(),
                                    Column(
                                        spacing=25,
                                        expand=True,
                                        controls=[
                                            Container(content=Row(
                            
                                user_Edit
                            ,expand=True,
                        ),expand=True),
                                            
                                        ],
                                    ),
                                        ],expand=True,alignment="center",horizontal_alignment="center"
                                    )
                        ],expand=True,
                    ),expand=True,visible=False),
        Container(content=Row(
                        [
                            Column(controls=[
                                    Row([Text(value="SENHAS",size=50)], alignment="center"),
                                    Row(
                                        [
                                            ElevatedButton(color=colors.WHITE,bgcolor=colors.GREEN_400,width=600,icon=icons.ADD,text='GERAR NOVA SENHA',on_click=menu_add_senhas,style=ButtonStyle(shape={"hovered": RoundedRectangleBorder(radius=20),"": RoundedRectangleBorder(radius=5)}))
                                        ],width=1200,alignment="center"
                                    ),
                                    Divider(),
                                    Column(
                                        spacing=25,
                                        expand=True,
                                        controls=[
                                            lista_senhas,
                                        ],
                                    ),
                                        ],expand=True,alignment="center",horizontal_alignment="center"
                                    )
                        ],expand=True,
                    ),expand=True),
    ]

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
        leading=btn_gerar,
        group_alignment=-1,
        trailing = btn_logout,
        destinations=[
            NavigationRailDestination(
                icon=icons.ACCOUNT_CIRCLE, label="PERFIL"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.KEY),label="SENHAS",
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
        elif page.route == "/redefinir":
            AppBarMenu.title = Text("Redefinição de Senha")
            AppBarMenu.leading = None
            page.views.append(
                View(
                    "/redefinir",
                    [
                        AppBarMenu,
                        Container(content=Row(
                            [
                                Column(controls=[
                                        Container(content=titulo_redefinir_senha,width=500,alignment=alignment.center_left,margin=margin.only(bottom=15)),
                                        Row([email_cadastrado,botao_verificar_email],alignment="center"),nova_senha,botao_alterar_senha
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
                            Row([rail,VerticalDivider(width=1),Column(pages,expand=True)],expand=True),
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