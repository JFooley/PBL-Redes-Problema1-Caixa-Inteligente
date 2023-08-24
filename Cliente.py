import socket
import threading

# Método principal do cliente, que envia as solicitações
def clienteSender(socketCliente):
    loop = True
    try:
        while loop:
            entrada = input("Leitura: ")
            
            # Fecha a comunicação
            if entrada.lower == 'exit':
                loop = False

            # Envio 
            socketCliente.send(entrada.encode())

    except socket.error as e:
        print(e)
    finally:
        socketCliente.close()

# Método que recebe e mostra nas telas as respostas
def clienteListner(socketCliente, host):
    loop = True
    try:
        while loop:
            # Resposta         
            Resposta = socketCliente.recv(1024).decode()
            print(Resposta)

    except socket.error as e:
        print(e)
    finally:
        socketCliente.close()

# Configurações do servidor
host = '26.191.37.90'  
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

