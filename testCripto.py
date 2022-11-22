import os,base64;#base 64: para encode, random:vetor de 16 bits randomico
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes;

def encrypt(mensagem):
    cipher = Cipher(algorithms.AES(os.urandom(32)), modes.CBC(os.urandom(16)))
    mensagem = base64.b64encode(mensagem.encode()).decode() #transformar mensagem em base 64 para fugir de problema de encode
    for i in range( 16 - (len(mensagem)  % 16) ): #adequar mensagem ao tamanho
        mensagem += " ";
    encryptor = cipher.encryptor(); 
    return encryptor.update(mensagem.encode("utf-8")) + encryptor.finalize();

criptografado = encrypt("");
print(criptografado);