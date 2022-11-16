import sqlite3

# Criação banco de dados
def create_DB():
    conexao = sqlite3.connect('Password-Manager/usuarios.db')
    c = conexao.cursor()
    c.execute('''CREATE TABLE user_cadastro (
            username text,
            email text,
            senha text
            )
        ''')
    conexao.commit()
    conexao.close()

# Importação das variáveis
def init(c, p):
    global components, page
    components = c
    page = p

# Cadastro de usuário
def cadastrar_usuario(e):
        cadastro = {
            'username': components['username'].current.value,
            'email':  components['email'].current.value,
            'senha':  components['senha'].current.value
        }
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

        

#  Login de usuário
def login_sistema(e):
        from flet import Text, AlertDialog
        '''
            Autenticar Login
        '''
        login = {
            'username': components['l_user'].current.value,
            'senha': components['l_senha'].current.value
        }
        conexao = sqlite3.connect('Password-Manager/usuarios.db')      
        
        c = conexao.cursor()
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