import sqlite3
from flet import Text, AlertDialog
# Criação banco de dados

def create_DB():
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


def init(c, p):
    global components, page
    components = c
    page = p

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
def cadastrar_usuario(e):
        cadastro = {
            'username': components['username'].current.value,
            'email':  components['email'].current.value,
            'senha':  components['senha'].current.value
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

        

#  Login de usuário
def login_sistema(e):
        '''
            Autenticar Login
        '''
        login = {
            'username': components['l_user'].current.value,
            'senha': components['l_senha'].current.value
        }
        conexao = sqlite3.connect('usuarios.db')      
        
        c = conexao.cursor()
        try:
            c.execute("SELECT senha FROM user_cadastro WHERE username = '{}'".format(login['username']))
            senha_bd = c.fetchall()
            conexao.close()
            if login['senha'] == senha_bd[0][0]:
                dlg = AlertDialog(title=Text(f"Hello {login['username']}!"),on_dismiss=lambda e: print("Dialog dismissed!"))
                page.dialog = dlg
                dlg.open = True
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