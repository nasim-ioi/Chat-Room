# betoone hamzaman chanta payam begire
# va in joori nabashe ke bad az in ke 
# ye doone gereft bekhad javab bede

import socket
import time

IP = '192.168.43.16'
PORT = 1323
#loozoomy nadare port server va client yeki bashe
#yani server rooye ye port shonood mikone client rooye ye port dige javab mide

client_socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)

client_socket.connect((IP, PORT))

while True:
    while True:
        message = client_socket.recv(1024)
        print(message.decode("utf-8"))
        time.sleep(5)
    msg = input('->')
    client_socket.send(bytes(msg , 'utf-8'))
    time.sleep(5)
client_socket.close()