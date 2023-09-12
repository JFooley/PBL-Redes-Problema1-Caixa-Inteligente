import json
import sys
import mercury
import socket

def lerTags(socket):
    epcs = map(lambda tag: tag, reader.read())
    tags = []
    for tag in epcs:
        tags.append(tag.epc.decode())
    socket.send(json.dumps(tags).encode())

# Cria o socket e associa a porta e host
socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind(('172.16.103.0', 2598))
socketServer.listen()

# configura a leitura na porta serial onde esta o sensor
param = 2300
if len(sys.argv) > 1:
    param = int(sys.argv[1])

reader = mercury.Reader("tmr:///dev/ttyUSB0")
reader.set_region("NA2")
reader.set_read_plan([1], "GEN2", read_power=param)

while True:
    socketDiretoCliente, enderecoCliente = socketServer.accept()

    lerTags(socketDiretoCliente)

    socketDiretoCliente.close()