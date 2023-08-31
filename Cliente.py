import socket
import threading
import json
import os

carrinho = []

# Método principal do cliente, que envia as solicitações
def clienteSender(socketCliente : socket):
    loop = True
    try:
        while loop:
            entrada = input()

            dictResponse = {'type':'codigo', 'content':''}

            # Fecha a comunicação
            if entrada.lower() == 'sair':
                loop = False
                continue
            elif entrada.lower() == 'comprar':
                dictResponse['type'] = 'comprar'
                dictResponse['content'] = carrinho

                entradaJson = json.dumps(dictResponse)
                socketCliente.send(entradaJson.encode())
                
                carrinho.clear()
            else:
                dictResponse['type'] = 'codigo'
                dictResponse['content'] = entrada

                entradaJson = json.dumps(dictResponse)
                socketCliente.send(entradaJson.encode())

    except socket.error as e:
        print(e)
    finally:
        print('Conexão encerrada')
        socketCliente.close()

# Método que recebe e mostra nas telas as respostas
def clienteListner(socketCliente, host):
    loop = True
    try:
        while loop:
            # Resposta         
            resposta = socketCliente.recv(1024).decode()
            
            os.system('cls')

            if 'nome' in resposta:
                carrinho.append(json.loads(resposta))
            else:
                print(resposta + "\n")

            total = 0
            print('Carrinho: ')
            for item in carrinho:
                print(item['nome'])
                total += item['preco']
            print(f'----------------------\nTotal: {total} R$')


    except socket.error as e:
        print(e)
    finally:
        socketCliente.close()

# Configurações do servidor
host = input('Digite o host do servidor: ')
port = 12345

socketCliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta no socket
    socketCliente.connect((host, port))
    print(f'Cliente conectado ao server {host}{port}')

    # Chama a função do cliente
    threadClienteListner = threading.Thread(target=clienteListner, args=(socketCliente, host))
    threadClienteListner.start()
    clienteSender(socketCliente)

except socket.error as e:
    print(e)

