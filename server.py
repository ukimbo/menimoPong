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

def read_pos(string): #takes string tuple and converts it to an actual tuple of integers
    string = str.split(",")
    return int(string[0]), int(string[1])
def make_pos(tup): #takes tuple of integers and converts it into a string
    return str(tup[0]) + "," + str(tup[1]) 

pos = [(1260, 410), (10, 410)]

def threaded_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode()) 
            pos[player] = data
            if not data: #if the client sends 0 information, disconnection is assumed
                print("Opponent Disconnected :(")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending to: ", reply)
            conn.sendall(str.encode(make_pos(reply))) #encodes information before sending it back over to the sever
        except:
            break
    print("Lost Connection")
    conn.close()

curr_player = 0
while True:
    conn, addr = s.accept() #conn is the object that is connected while addr is the IP address
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, curr_player))
    curr_player += 1

