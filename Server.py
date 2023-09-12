import json
import requests
import socket
import threading
from Config import portaServidor, hostServidor, ipDatabase

# Thread para cuidar de cada cliente individualmente
def handleSolicitacoes(socketDiretoCliente, enderecoCliente):
    try:
        # Busca todas as conexões atuais
        conexoes = requests.get(ipDatabase + 'caixas')
        conexoesJson = conexoes.json()

        # Verifica se aquela conexão não existe na lista
        if enderecoCliente[0] not in list(conexoesJson.keys()):
            conexão = {enderecoCliente[0] : True}
            requests.post(ipDatabase + 'update-caixa', json=conexão)
            
        # Trata o caso em que o caixa está bloqueado
        elif conexoesJson[enderecoCliente[0]] == False:
            refuseMSG = 'Caixa bloqueado!'
            socketDiretoCliente.send(refuseMSG.encode())
            return
        
        while True:            
            data = socketDiretoCliente.recv(1024)
            request : str = data.decode()
            requestJson : dict = json.loads(request)

            print(f'{enderecoCliente}->: {requestJson["type"]} : {requestJson["content"]}')

            # Realiza a compra
            if requestJson["type"] == 'comprar':
                dataSize = requestJson['content']
                socketDiretoCliente.send('100'.encode())

                # Recebe toda a lista do carrinho
                requestContent = ''
                while len(requestContent) < dataSize:
                    piceSize = min(1024, (dataSize - len(requestContent)))
                    pieceData = socketDiretoCliente.recv(piceSize).decode()
                    requestContent += pieceData
                    print(f'{enderecoCliente}->: {requestJson["type"]} : {requestContent}')
                
                # Post da compra
                compraContentJson = json.loads(requestContent)
                respostaAPI = requests.post(ipDatabase + 'comprar', json=compraContentJson)

                # Post para atualizar o carrinho como vazio
                updateContentJson = {f'{enderecoCliente[0]}{enderecoCliente[1]}' : []}
                requests.post(ipDatabase + 'update-carrinho', json=updateContentJson)
            
            # Resgata as informações de um produto a partir do código
            elif requestJson['type'] == 'codigo':
                respostaAPI = requests.get(ipDatabase + requestJson["content"])

            # Atualiza o carrinho no servidor
            elif requestJson['type'] == 'update-carrinho':
                dataSize = requestJson['content']
                socketDiretoCliente.send('100'.encode())

                # Recebe toda a lista do carrinho
                requestContent = ''
                while len(requestContent) < dataSize:
                    piceSize = min(1024, (dataSize - len(requestContent)))
                    pieceData = socketDiretoCliente.recv(piceSize).decode()
                    requestContent += pieceData
                    print(f'{enderecoCliente}->: {requestJson["type"]} : {requestContent}')
                
                compraContentJson = json.loads(requestContent)

                # Post para atualizar o carrinho como vazio
                updateContentJson = {f'{enderecoCliente[0]}{enderecoCliente[1]}' : compraContentJson}
                requests.post(ipDatabase + 'update-carrinho', json=updateContentJson)
            
            # Pós response
            if respostaAPI.status_code == 200 or respostaAPI.status_code == 201:
                responseJson = respostaAPI.json()
                dataResponse = json.dumps(responseJson)
                socketDiretoCliente.send(dataResponse.encode())
            else:
                erroMSG = 'Erro na requisição'
                socketDiretoCliente.send(erroMSG.encode())
            
    except Exception as e:
        print(f'Conexão com {enderecoCliente} interrompida devido a:')
        print(e) 

# Cria o socket e associa a portaServidora e host
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((hostServidor, portaServidor))
socketServer.listen()
print('Servidor iniciado em', hostServidor)

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
