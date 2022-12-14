import sqlite3

# def insert():
#     conexao = sqlite3.connect('C:/WORKSPACE/MYPROJECTS/Password-Manager/usuarios_test.db')
#     c = conexao.cursor()
#     query = f"INSERT INTO user_senhas(nome, desc, senha) VALUES (?, ?, ?)"
#     valores = (1,2,3)
#     c.execute(query,valores)
#     conexao.commit()
#     conexao.close()

user_logado = 1
# insert()
def verificar_senhas_user():
    dados_cadastrados = []
    conexao = sqlite3.connect('C:/WORKSPACE/MYPROJECTS/Password-Manager/usuarios.db')
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

print(verificar_senhas_user())
[
    (('abc',), ('123',), ('123',)),                                 0   
    (('oioi',), ('oioi',), ('Wez/oKkq2xU=',)),                      1
    (('esfdsf',), ('sdfsdfsdf',), ('N8mYudPbhI/nU+Fz3BiZ',)),       2
    (('nome',), ('desc',), ('senha',))                              3
]