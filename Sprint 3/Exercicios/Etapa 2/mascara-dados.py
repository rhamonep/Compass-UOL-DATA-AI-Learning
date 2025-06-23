import hashlib

while True:

    try:

        texto = input("Digite uma string (ou pressione Ctrl+C para sair): ")

        hash_obj = hashlib.sha1(texto.encode())

        print("Hash SHA-1:", hash_obj.hexdigest())

    except EOFError:

        print(
            "\nErro: entrada inesperada (possivelmente executado sem terminal interativo).")
