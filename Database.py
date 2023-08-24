from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from Dados import dados

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pathTratado = self.path.split('/')
        if pathTratado[1] != '':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                response = dados[pathTratado[1]]
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))
            except:
                response = 'Produto inexistente 1'
                self.wfile.write(bytes(json.dumps(response), 'utf-8'))

        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        pathTratado = self.path.split('/')
        


# Cria e inicializa o server do "banco de dados"
server_address = ('', 8000)
serverHTTP = HTTPServer(server_address, APIHandler)
serverHTTP.serve_forever()