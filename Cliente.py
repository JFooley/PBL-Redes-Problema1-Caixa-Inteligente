import socket
import json
import os
from Config import hostRFIDcliente, portaRFID, portaServidor

carrinho = []

# Envia todo o carrinho local do cliente para o server
def mandarCarrinho(args : str):
    dictUpdate = {'type': args, 'content':''}
    dictUpdate['content'] = len(json.dumps(carrinho))

    # Envia o tamanho dos dados do carrinho
    entradaJson = json.dumps(dictUpdate)
    socketServidor.send(entradaJson.encode())

    # Espera a confirmação do server e envia o carrinho
    respostaCompra = socketServidor.recv(1024).decode()
    if respostaCompra == '100':
        carrinhoJson = json.dumps(carrinho)
        socketServidor.sendall(carrinhoJson.encode())

# Ouve a resposta do server
def ouvirResponse():
    resposta = socketServidor.recv(1024).decode()

    os.system('cls')
    os.system('clear')

    if 'nome' in resposta:
        carrinho.append(json.loads(resposta))
    else:
        print(resposta + "\n")

    total = 0
    print('Carrinho: ')
    for item in carrinho:
        print(f"{item['nome']} - {item['preco']} R$")
        total += item['preco']
    print(f'----------------------\nTotal: {total} R$')

# Método principal do cliente, que envia as solicitações
def clienteRoutine():
    loop = True
    try:
        while loop:
            entrada = input("1- Comprar\n2- Ler produtos")

            dictResponse = {'type':'', 'content':''}

            # Comprar
            if entrada.lower() == '1':
                mandarCarrinho('comprar')
                carrinho.clear()
                ouvirResponse()

            # Ler o sensor
            elif entrada.lower() == '2':                
                dictResponse['type'] = 'codigo'

                try:
                    # Se conecta ao sensor e realiza a leitura
                    socketRFID = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    socketRFID.connect((hostRFIDcliente, portaRFID))
                    
                    tagsListaCru = socketRFID.recv(1024).decode()
                    tagsLista = json.loads(tagsListaCru)

                    for tag in tagsLista:
                        dictResponse['content'] = tag
                        
                        entradaJson = json.dumps(dictResponse)
                        socketServidor.send(entradaJson.encode())

                        ouvirResponse()
                    
                    socketRFID.close()

                    # Atualiza o estado do carrinho no DB
                    mandarCarrinho('update-carrinho')
                    ouvirResponse()

                except Exception as e:
                    print(e)

    except Exception as e:
        print(e)
    finally:
        print('Conexão encerrada')
        socketServidor.close()

# Configurações do servidor
hostServidor = input('Digite o hostServidor do servidor: ')

socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Conecta nos sockets
    socketServidor.connect((hostServidor, portaServidor))
    print(f'Cliente conectado ao server {hostServidor}{portaServidor}')
    
    clienteRoutine()

except socket.error as e:
    print(e)

