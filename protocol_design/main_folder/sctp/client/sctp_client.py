import socket 
import sctp
import os

class SCTPclient:
  def __init__(self,serv_ip,serv_port):
    
    # Initialize the socket
    self.ip = serv_ip
    self.port = serv_port
    self.dataSize = 40000
   
  def makeRequest(self,req):
    print(req)
    sock = sctp.sctpsocket_tcp(socket.AF_INET)
    self.socket = sock
    self.socket.connect((self.ip,self.port))

    self.socket.sctp_send(req.encode())
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

client = SCTPclient("127.0.0.1",8080)
client.makeRequest("GET /cat.jpg HTTP 1.0")
client.close_connection()
