'''
AES ESPECIFICAÇÃO PARA CRIPTOGRAFIA DE DADOS ESTABELECIDA PELA NIST (ORGAO DE NORMAS).
AES É CRIPTOGRAFIA DE BLOCO.VETOR DE INICIALIZAÇÃO RANDOMICO.
'''
import os, uuid, random, base64;#base 64: para encode, random:vetor de 16 bits randomico
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes;

class AesHelper:#criação de classe
    def __init__(self, key=None, iv=None):#criação do construtor, pode usar uma key ou nap
        if key == None:
            self.key = os.urandom(32);#256 bits
        if iv == None:
            self.iv = os.urandom(16);
        self.cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv));#selc tipo algoritmo AES precisa de um construtor
    def encrypt(self, mensagem): 
        mensagem = base64.b64encode(mensagem.encode()).decode(); #transformar mensagem em base 64 para fugir de problema de encode
        for i in range( 16 - (len(mensagem)  % 16) ): #adequar mensagem ao tamanho
            mensagem += " ";
        encryptor = self.cipher.encryptor(); 
        return encryptor.update(mensagem.encode("utf-8")) + encryptor.finalize();
    def decrypt(self, message):
        decryptor = self.cipher.decryptor();
        return  base64.b64decode( (decryptor.update(message) + decryptor.finalize()) ).decode("utf-8").strip();
        #retorna  a mensagem

ae = AesHelper();#instancia
criptografado = ae.encrypt("danilofigueiredoicen");
print(criptografado);
print(ae.decrypt(criptografado));