import hashlib

while True:

    texto = input("Digite uma string (ou pressione Ctrl+C para sair): ")

    hash_obj = hashlib.sha1(texto.encode())

    print("Hash SHA-1:", hash_obj.hexdigest())