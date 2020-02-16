import socket
import time
import select

IP = ''
PORT = 8217

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((IP, PORT))

server_socket.listen(10)
# print(server_socket)
 print("server up!")

socket_list = [server_socket]

clients = {}


while True:
    read_socket, write_socket, exception_socket = select.select(
        socket_list, [], socket_list)
    #print("read_socket", read_socket)
    for s in read_socket:
        if s == server_socket:
            client_socket, address = server_socket.accept()

            if client_socket:
                client_socket.send(bytes("username? , your username contact?", 'utf-8'))
                msg = client_socket.rec(1024).decode('utf-8')
                value_list = msg.split(',')
                if value_list[0] in status:
                    client_socket.send(bytes("this username has already exist pleas connect again", 'utf-8'))
                    client_socket.close()
                else:
                    socket_list.append(client_socket)
                    print("Connection Established from {}".format(address))
                    if value_list[1] not in status:
                        client_socket.send(bytes("this username is offline", 'utf-8'))
                    else:
                        if    
                #user = address[0]
                        clients[client_socket] = []
                # for client_sockets in clients:
                #     if client_sockets != client_socket:
                #         client_sockets.send(
                #             bytes("{} joined Group!".format(address), 'utf-8'))

        else:
            message = s.recv(1024)
            if not message:
                socket_list.remove(s)
                del clients[s]
                continue
          #  print(message.decode('utf-8'))
            for client_socket in clients:
                if client_socket != s:
                    client_socket.send(message)
    for s in exception_socket:
        socket_list.remove(s)
        del clients[s]
    print("socket list \n", socket_list)
# server_socket.close()
