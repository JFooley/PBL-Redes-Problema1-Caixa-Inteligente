from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import copy
import datetime as date

lock = threading.Lock()

# Dados
dados = {
    'E20000172211010218905459': {'nome' : 'Arroz'  , 'codigo' : 'E20000172211010218905459', 'preco' : 5.50, 'stock' : 10},
    'E20000172211010118905454': {'nome' : 'Carne'  , 'codigo' : 'E20000172211010118905454', 'preco' : 20.0, 'stock' : 10},
    'E20000172211011718905474': {'nome' : 'Leite'  , 'codigo' : 'E20000172211011718905474', 'preco' : 6.00, 'stock' : 10},
    'E2000017221101321890548C': {'nome' : 'Ovo'    , 'codigo' : 'E2000017221101321890548C', 'preco' : 0.50, 'stock' : 10},
    'E20000172211009418905449': {'nome' : 'Feijão' , 'codigo' : 'E20000172211009418905449', 'preco' : 9.50, 'stock' : 10},
    'E20000172211012518905484': {'nome' : "Laranja", 'codigo' : 'E20000172211012518905484', 'preco' : 3.00, 'stock' : 10},
    'E20000172211011118905471': {'nome' : "Uva"    , 'codigo' : 'E20000172211011118905471', 'preco' : 7.99, 'stock' : 10},
    'E2000017221101241890547C': {'nome' : "Pera"   , 'codigo' : 'E2000017221101241890547C', 'preco' : 2.50, 'stock' : 10},
    'E2000017221100961890544A': {'nome' : "Kiwi"   , 'codigo' : 'E2000017221100961890544A', 'preco' : 6.75, 'stock' : 10},
}

# {'ip' : status (boleano)}
caixas = {}

# {'ip' : [carrinho]}
carrinhos = {}

# {'data' : dataHoje, 'carrinho' : carrinho}
compras = []

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

        # Rota que retorna os caixas e seu status
        elif pathTratado[1] == 'carrinhos':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = carrinhos
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # Rota para listar o histórico de compras
        elif pathTratado[1] == 'compras':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            response = compras
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
                # Verifica se a compra é possivel
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
                    
                # Confirma a compra
                dados.update(tempDados)

                # Salva a compra no histórico
                dataHoje = date.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                compra = {'data' : dataHoje, 'carrinho' : jsonRecebido}
                compras.append(compra)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = 'Compra realizada'
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        # Rota que atualiza o status do caixas
        elif pathTratado[1] == 'update-caixa':
            with lock:
                caixas.update(jsonRecebido)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
        
        # Rota que atualiza o carrinho 
        elif pathTratado[1] == 'update-carrinho':
            with lock:
                carrinhos.update(jsonRecebido)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = 'Teste update'
            self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            
# Cria e inicializa o server do "banco de dados"
print('Database iniciado')
server_address = ('', 8000)
serverHTTP = HTTPServer(server_address, APIHandler)
serverHTTP.serve_forever()
