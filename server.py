import socket, sys
from _thread import *

server = "10.0.0.149" #For LAN connetions, this IP address has to be the same as the device running the server script
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port)) #Binds server IP to the given port argument
except socket.error as e:
    print(e) #prints error

s.listen(2) #Opens up port, allowing multiple clients to connect, in this case 2
print("Queued for Match, Waiting for oppenent...")

def threaded_client(conn):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(2048) #Data received by incoming client connection
            reply = data.decode("utf-8") #Data must be decode because data is encoded when sent to server
            if not data: #if the client sends 0 information, disconnection is assumed
                print("Opponent Disconnected :)")
                break
            else:
                print("Received: ", reply)
                print("Sending to: ", reply)
            conn.sendall(str.encode(reply)) #encodes information before sending it back over to the sever
        except:
            break
    print("Lost Connection")
    conn.close()

while True:
    conn, addr = s.accept() #conn is the object that is connected while addr is the IP address
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))

