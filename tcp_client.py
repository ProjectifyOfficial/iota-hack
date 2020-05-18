import socket   
import time            
 
sock = socket.socket()

#esp32 server details
host = "192.168.0.138" 
port = 80              
time.sleep(10);
sock.connect((host, port))
 
message = "Fulfill service"
sock.send(message.encode())
 
sock.close()