from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from Dados import dados, caixas

# Exemplo do esquema dos caixas
# {'26.191.37.90' : True}

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
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            dadosTemp = dados
            for item in jsonRecebido:
                if dadosTemp[item['codigo']]['stock'] > 0:
                    dadosTemp[item['codigo']]['stock'] -= 1
                else:
                    response = 'Estoque insuficiente!'
                    self.wfile.write(bytes(json.dumps(response), 'utf-8'))
                    return
            dados.update(dadosTemp)

            response = 'Compra realizada'
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # Rota que atualiza o status do caixas
        elif pathTratado[1] == 'update-caixa':
            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            caixas.update(jsonRecebido)
            print(caixas)

            
# Cria e inicializa o server do "banco de dados"
print('Database iniciado')
server_address = ('', 8000)
serverHTTP = HTTPServer(server_address, APIHandler)
serverHTTP.serve_forever()
