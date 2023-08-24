import json
import requests
import socket
import threading

# Thread para cuidar de cada cliente individualmente
def handleSolicitacoes(socketDiretoCliente, enderecoCliente):
    try:
        while True:            
            # Recebe
            data = socketDiretoCliente.recv(1024)
            codigo = data.decode()
            print(f'{enderecoCliente}->: {codigo}')

            # Chama a API
            respostaAPI = requests.get('http://localhost:8000/' + codigo)
            
            if respostaAPI.status_code == 200:
                responseJson = respostaAPI.json()
                dataResponse = json.dumps(responseJson)
                socketDiretoCliente.send(dataResponse.encode())
            else:
                erroMSG = 'Erro na requisição'
                socketDiretoCliente.send(erroMSG.encode())
    except:
        print(f'Conexão com {enderecoCliente} interrompida')
    
# Configurações do servidor
host = '26.191.37.90'  
port = 12345

# Cria o socket e associa a porta e host
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((host, port))
socketServer.listen()
print('Servidor iniciado')

threadsClientes = []

loop = True
while loop:
    # Aceita a conexão do cliente
    socketDiretoCliente, enderecoCliente = socketServer.accept()
    print(f'Conexão com o cliente {enderecoCliente} aceita')

    # Cria uma thread específica 
    threadCliente = threading.Thread(target=handleSolicitacoes, args=(socketDiretoCliente, enderecoCliente))
    threadCliente.start()

    threadsClientes.append(threadCliente)



