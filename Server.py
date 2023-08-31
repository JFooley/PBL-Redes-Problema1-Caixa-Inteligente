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
            request : str = data.decode()
            requestJson : dict = json.loads(request)

            print(f'{enderecoCliente}->: {requestJson["type"]} : {requestJson["content"]}')

            if requestJson["type"] == 'comprar':
                respostaAPI = requests.post('http://localhost:8000/comprar', json=requestJson["content"])
            else:
                respostaAPI = requests.get('http://localhost:8000/' + requestJson["content"])

            if respostaAPI.status_code == 200 or respostaAPI.status_code == 201:
                responseJson = respostaAPI.json()
                dataResponse = json.dumps(responseJson)
                socketDiretoCliente.send(dataResponse.encode())
            else:
                erroMSG = 'Erro na requisição'
                socketDiretoCliente.send(erroMSG.encode())
            
    except:
        print(f'Conexão com {enderecoCliente} interrompida')
    
# Configurações do servidor
host = socket.gethostbyname(socket.gethostname()) 
port = 12345

# Cria o socket e associa a porta e host
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((host, port))
socketServer.listen()
print('Servidor iniciado em', host)

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



