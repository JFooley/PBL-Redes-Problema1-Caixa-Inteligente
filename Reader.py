import json
import sys
import mercury
import socket
from Config import hostRFID, portaRFID

def lerTags(socket):
    epcs = map(lambda tag: tag, reader.read())
    tags = []
    for tag in epcs:
        tags.append(tag.epc.decode())
    socket.send(json.dumps(tags).encode())

def leituraTeste(socketDiretoCliente):
    tags = ['E20000172211010218905459',
            'E20000172211010118905454',
            'E20000172211011718905474',
            'E2000017221101321890548C',
            'E2000017221101241890547C']
    socketDiretoCliente.send(json.dumps(tags).encode())

# Cria o socket e associa a porta e host
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind((hostRFID, portaRFID))
socketServer.listen()

# configura a leitura na porta serial onde esta o sensor
param = 2300
if len(sys.argv) > 1:
    param = int(sys.argv[1])

# reader = mercury.Reader("tmr:///dev/ttyUSB0")
# reader.set_region("NA2")
# reader.set_read_plan([1], "GEN2", read_power=param)

while True:
    socketDiretoCliente, enderecoCliente = socketServer.accept()

    leituraTeste(socketDiretoCliente)

    # lerTags(socketDiretoCliente)

    socketDiretoCliente.close()