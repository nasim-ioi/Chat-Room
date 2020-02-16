import socket
import time

IP = ''
PORT = 4002

server_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
"""model IP"""  """ tcp or udp"""
server_socket.bind((IP , PORT)) 
#tuple pass mide #mire mishine roye in port va ip 
server_socket.listen()
soket_list = [server_socket]
#user ha ro negah midarim
clients = {}

while True:
    read_socket, write_socket, exception_socket = select.select(socket_list, [], socket_list)
    for s in read_socket:
        if s == server_socket:
            client_socket, address = server_socket.accept()
            if client_socket:
                client_socket.send(bytes("welcome" , "utf-8"))
                soket_list.append(client_socket)
                user = address[0] #list as ip va port kasi ke be ma vaslan
                clients[client_socket] = user
                print("connection established from {}".format(address))
        else:
            message = s.recv(1024)
            if not message:
                socket_list.remove(s)
                del clients[s]
                continue
            print(message.decode('utf-8'))
            for client_socket in clients:    
                if client_socket != s:    
                    #server hamzaman mibine
                    client_socket.send(message)
    for s in exception_socket:
            socket_list.remove(s)
            del clients[s]
server_socket.cloes()