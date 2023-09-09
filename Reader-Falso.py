import json
import sys
import socket
from Config import hostRFIDTeste, portaRFID

def leituraTeste(socketDiretoCliente):
    tags = ['E20000172211010218905459',
            'E20000172211010118905454',
            'E20000172211011718905474',
            'E2000017221101321890548C',
            'E2000017221101241890547C']
    socketDiretoCliente.send(json.dumps(tags).encode())

# Cria o socket e associa a porta e host
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((hostRFIDTeste, portaRFID))
socketServer.listen()

# configura a leitura na porta serial onde esta o sensor
param = 2300
if len(sys.argv) > 1:
    param = int(sys.argv[1])

print(f'Servidor do reader iniciado em {hostRFIDTeste}:{portaRFID}')

while True:
    socketDiretoCliente, enderecoCliente = socketServer.accept()

    print('Leitura iniciada')

    leituraTeste(socketDiretoCliente)

    print('Leitura finalizada')

    socketDiretoCliente.close()