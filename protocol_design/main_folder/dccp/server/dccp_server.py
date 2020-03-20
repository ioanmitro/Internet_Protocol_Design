import socket
from os import path

# General Settings
socket.DCCP_SOCKOPT_PACKET_SIZE = 1
socket.DCCP_SOCKOPT_SERVICE = 2
socket.SOCK_DCCP = 6
socket.IPROTO_DCCP = 33
socket.SOL_DCCP = 269
packet_size = 512

socket.DCCP_SOCKOPT_AVAILABLE_CCIDS = 12
socket.DCCP_SOCKOPT_CCID = 13
socket.DCCP_SOCKOPT_TX_CCID = 14
socket.DCCP_SOCKOPT_RX_CCID = 15


class DCCPserver:
    def __init__(self, servIp, servPort, conns):
        self.ip = servIp
        self.port = servPort
        self.dataSize = 40000
        # Initialize the socket and set some options
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP)
        self.socket.setsockopt(
            socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
        self.socket.setsockopt(
            socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind((self.ip, self.port))
        self.socket.listen(conns)

    def connection_close(self):
        self.socket.close()

    def checkFormat(self, req):
        if "GET" in str(req):
            return True
        else:
            return False

    def checkIfFileExists(self, filename):
        if path.exists(filename):
            return True
        else:
            return False

    def create_response(self, found, c, filename):
        if found == True:
            if "html" not in filename:
                print(found)
                with open('./'+filename, 'rb') as content_file:
                    content = content_file.read()
                c.send(b'HTTP/1.0 200 OK\nContent-Type: image\n\n')
                c.send(content)
                c.close()
            else:
                with open('./'+filename, 'r') as content_file:
                    content = content_file.read()
                c.send(b'HTTP/1.0 200 OK\nContent-Type: text/html\n\n')
                c.send(content.encode())
                c.close()
        else:
            c.send(b'HTTP/1.0 404 Not Found\nContent-Type: text/html\n\n')
            c.close()

    def fetch(self, client):

        # Retrieve the client's request
        req = client.recv(self.dataSize)

        # Check the format
        if(self.checkFormat(req)):

            # Tokenize the request
            tokens = req.decode('utf-8').split()

            # Retrieve the requested object
            if tokens[1] == '/':
                filename = "index.html"
            else:
                filename = tokens[1].replace("/", "")
            self.create_response(self.checkIfFileExists(
                filename), client, filename)
        else:
            client.send(b'HTTP/1.0 500 Internam Error\nContent-Type: text/html\n\n')
            client.send(b'ERROR')
            client.close()

    def run(self):

        while True:

            # Waiting for client to connect
            client, addr = self.socket.accept()
            self.fetch(client)


server = DCCPserver("127.0.0.1", 8080, 3)
print("server run")
server.run()
server.connection_close()
