import socket
import os

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


class DCCPclient:
    def __init__(self, servIp, servPort):
      self.dataSize = 40000
      self.ip = servIp
      self.port = servPort
 
    def makeRequest(self, req):
        
        #Initialize the socket
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_DCCP, socket.IPROTO_DCCP)
        self.socket = sock
        self.socket.setsockopt(
            socket.SOL_DCCP, socket.DCCP_SOCKOPT_PACKET_SIZE, packet_size)
        self.socket.setsockopt(
            socket.SOL_DCCP, socket.DCCP_SOCKOPT_SERVICE, True)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Connect
        self.socket.connect((self.ip, self.port))
  
        self.socket.send(req.encode())
        print(req)
        headers = self.socket.recv(self.dataSize)
        body = self.socket.recv(self.dataSize)
        if "200" in headers.decode('utf-8'):
            if "html" in headers.decode('utf-8'):
                body = body.decode("utf-8")
                tokens = req.split()
                filename = tokens[1].replace("/","")
                if filename == "":
                    filename="index.html"
                with open(filename,"w") as f:
                  f.write(body)
                os.system("firefox "+filename)
            else:
                tokens = req.split()
                filename = tokens[1].replace("/","")
                if filename == "":
                    filename="index.html"
                with open(filename,"wb") as f:
                    f.write(body)
                os.system("eog "+filename)
        elif "500" in headers.decode('utf-8'):
          print("Request is not valid")
          self.close_connection()
        else: 
          print("Requested file not found")
          self.close_connection()

    def close_connection(self):
        self.socket.close()

client = DCCPclient("127.0.0.1", 8080)
client.makeRequest("GET /cat.jpg HTTP 1.0")
client.makeRequest("GET / HTTP 1.0")

client.close_connection()
