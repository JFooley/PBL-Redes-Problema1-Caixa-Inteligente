from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import copy
from Dados import caixas, dados

lock = threading.Lock()

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pathTratado = self.path.split('/')

        # Rota que retorna os caixas e seu status
        if pathTratado[1] == 'caixas':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = caixas
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # Rota para listar os produtos
        elif pathTratado[1] != '':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                response = dados[pathTratado[1]]
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            except:
                response = 'Produto inexistente'
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # Rota que lista todo o database
        else:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = dados
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
    
    def do_POST(self):
        pathTratado = self.path.split('/')

        # Recebe corretamente a body enviada
        datasize = self.headers['Content-Length']
        dadosRecebidos = self.rfile.read(int(datasize))
        jsonRecebido = json.loads(dadosRecebidos.decode())

        # Rota que realiza a compra
        if pathTratado[1] == 'comprar':
            with lock:
                tempDados = copy.deepcopy(dados)
                for item in jsonRecebido:
                    if tempDados[item['codigo']]['stock'] > 0:
                        tempDados[item['codigo']]['stock'] -= 1
                    else:
                        self.send_response(201)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        response = 'Estoque insuficiente!'
                        self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                        return
                
                dados.update(tempDados)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = 'Compra realizada'
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # Rota que atualiza o status do caixas
        elif pathTratado[1] == 'update-caixa':
            with lock:
                caixas.update(jsonRecebido)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            
# Cria e inicializa o server do "banco de dados"
print('Database iniciado')
server_address = ('', 8000)
serverHTTP = HTTPServer(server_address, APIHandler)
serverHTTP.serve_forever()
