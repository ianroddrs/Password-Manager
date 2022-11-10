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