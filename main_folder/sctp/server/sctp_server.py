import socket
import sctp
from os import path
import binascii

class SCTPserver:
  def __init__(self,serv_ip,serv_port,conns):
    
    # Initialize the server parameters
    self.ip = serv_ip
    self.port = serv_port
    self.connections = conns
  
    # Create the server
    sock = sctp.sctpsocket_tcp(socket.AF_INET)
    sock.events.clear()
    sock.bind((self.ip,self.port))
    sock.listen(self.connections)
    
    self.socket = sock
    self.dataSize = 40000

  def checkFormat(self,req):
    if "GET" in str(req):
      return True
    else:
      return False 
  
  def checkIfFileExists(self,filename):
    if path.exists(filename):
      return True
    else:
      return False

  def create_response(self, found, c, filename):
    if found == True:
      if "html" not in filename:
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

  def fetch(self,client):

    # Retrieve the client's request
    req = client.recv(self.dataSize)
    print(req.decode("utf-8")) 
    # Check the format
    if(self.checkFormat(req)):
      
      # Tokenize the request 
      tokens = req.decode('utf-8').split()
      
      # Retrieve the requested object 
      if tokens[1] == '/':  
        filename = "index.html"
      else:
        filename = tokens[1].replace("/","")
      self.create_response(self.checkIfFileExists(filename),client,filename)
    else:
      client.send(b'HTTP/1.0 500 Internam Error\nContent-Type: text/html\n\n')
      client.send(b'ERROR')
      client.close()

  def run(self):
    
    while True:
      
      # Waiting for client to connect
      client,addr = self.socket.accept()
      
      # Fetch data with socket
      self.fetch(client)
  
  def connection_close(self):
    self.socket.close()

server = SCTPserver("127.0.0.1",8080,4)
print("server run")
server.run()
server.connection_close()
