import socket
import time
import select
import threading
import datetime
# import sqlite3
# import ChatroomDatabase as DC
from ChatroomDatabase import DataBaseConnection as DBC
from ChatroomDatabase import DataBaseCursor as DC

IP = ''
PORT = 5722

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)# in khodesh port ro mibande (should be searched)

server_socket.bind((IP, PORT))

server_socket.listen(10)
print("server up!")

socket_list = [server_socket]

clients = {}

conn = DBC()
cursor = DC(conn)
# conn = sqlite3.connect("ChatroomDatabased.db")
# cursor.execute("DROP TABLE users")
# cursor.execute("DROP TABLE chats")
# conn.commit()

cursor.execute("CREATE TABLE IF NOT EXISTS users(pid INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255) NOT NULL, contact VARCHAR(255) DEFAULT NULL, state VARCHAR(255) DEFAULT 'free', status VARCHAR(255) DEFAULT 'offline')")
cursor.execute("CREATE TABLE IF NOT EXISTS chats(sender VAECHAR(255), receiver VARCHAR(255) , message TEXT , date TEXT)")

conn.commit()


# cursor.execute("CREATE TABLE IF NOT EXISTS chats(sender VAECHAR(255) , FOREIGN KEY(sender) REFERENCES users(pid), receiver VARCHAR(255) , message TEXT , date TEXT)")
# conn.commit()

cursor.execute("SELECT * FROM users")
a = cursor.fetchall()
print(" ------ ", a)

cursor.execute("SELECT * FROM chats")
a = cursor.fetchall()
print(" ****** ", a)


def AskUsername(client_socket):

    # conn = sqlite3.connect("ChatroomDatabased.db")
    # conn = DC.DataBaseConnection()
    # cursor = conn.cursor()
    conn = DBC()
    cursor = DC(conn)

    client_socket.send(bytes("Enter Your Name : ", 'utf-8'))
    try:
        user = client_socket.recv(1024).decode("utf-8")

    except:
        # Update2(client_socket, conn, cursor)
        Update2(client_socket)

    else:
        clients[client_socket] = (user, None)
        # print("i am here #### ")
        cursor.execute("SELECT * FROM users WHERE username = ?", (user,))
        if not len(cursor.fetchall()):
            cursor.execute("INSERT INTO users(username, status) VALUES(?, 'online')", (user,))
        else:
            cursor.execute("UPDATE users SET state = 'free', status = 'online' WHERE username = ? ", (user,))
        conn.commit()

        t1 = threading.Thread(target = findContact , args = (client_socket, user))
        t1.start()
    finally:
        return

def findReceiver(s):
    for client_socket in clients.keys():
        if clients[client_socket][0] == clients[s][1]:
            return(client_socket)

def Update1(client_socket, user, contact):
    # conn = conn
    # cursor = cursor
    cursor.execute("UPDATE users SET contact = ?, state = 'busy' WHERE username = ?", (contact, user))
    conn.commit()
    clients[client_socket] = (user, contact)

def Update2(s):

    # conn = conn
    # cursor = cursor

    print("I am in Update2")
    try:
        client_socket = findReceiver(s)
        try:
            client_socket.send(bytes("your connection with your contact was interupted", 'utf-8'))
        except:
            print("this person talked with himself")
            pass
        else:
            cursor.execute("UPDATE users SET state = 'free', status = 'online' WHERE username = ?", (clients[client_socket][0],))
            t = threading.Thread(target = findContact , args = (client_socket, clients[client_socket][0]))
            t.start()
        finally:
            cursor.execute("UPDATE users SET status = 'offline' WHERE username = ?", (clients[s][0],))
            conn.commit()
    except:
        print("in Update2 an error eccured")
        pass
    finally:
        return

def findContact(client_socket, user):
    # conn = sqlite3.connect("ChatroomDatabased.db")
    # conn = DC.DataBaseConnection()
    # cursor = conn.cursor()
    conn = DBC()
    cursor = DC(conn)

    try:
        while True:
            client_socket.send(bytes("Who do you want to chat with?", 'utf-8'))
            contact = client_socket.recv(1024).decode("utf-8")
            cursor.execute("SELECT * FROM users WHERE username = ?", (contact,))
            contact_info = cursor.fetchall()
            if len(contact_info):

                if contact_info[0][4] == 'offline':
                    client_socket.send(bytes("this person is offline", 'utf-8'))

                else:

                    if contact_info[0][3] == 'busy':

                        if contact_info[0][2] == user:
                            Update1(client_socket, user, contact)
                            return
                        
                        else:
                            client_socket.send(bytes("this person is busy", 'utf-8'))
                    
                    else:
                        Update1(client_socket, user, contact)
                        return
            else:
                client_socket.send(bytes("this person does not exist", 'utf-8'))

    except:
        print("an error eccured in findContact")
        Update2(client_socket)

    finally:
        return


while True:
    read_socket, write_socket, exception_socket = select.select(socket_list, [], socket_list)

    for s in read_socket:
        if s == server_socket: #darkhast tcp connection (server socket ye object ke ijad mishe)

            client_socket, address = server_socket.accept() 
            if client_socket:  

                client_socket.send(bytes("welcome!", 'utf-8'))
                
                print("Connection Established from {}".format(address))

                t = threading.Thread(target=AskUsername, args=(client_socket,))
                t.start()

                socket_list.append(client_socket)
    
        else:
            try:
                message = s.recv(1024)
            except:
                # if not message:
                print("NOt message")
                Update2(s)
                try:
                    socket_list.remove(s)
                    del clients[s]
                except:
                    pass
                continue
            else:
                conn = DBC()
                cursor = DC(conn)
                client_socket = findReceiver(s)
                client_socket.send(message)
                cursor.execute("INSERT INTO chats(sender, receiver, message, date) VALUES(?, ?, ?, ?)", (clients[s][0], clients[client_socket][0], message.decode('utf-8'), str(datetime.datetime.now())))
                conn.commit()
            
    for s in exception_socket:
        Update2(s)
        try:
            socket_list.remove(s)
            del clients[s]
        except:
            pass
    
    # print("the total number of thread : " , threading.active_count()) 
    # raje be khat bala bayad fekr konam
    # chera bayad hatman vasl she yki behesh ta tedad thread ha ro bege?
    # va in ke chera tedad thread ha oon mishe?
    time.sleep(2)

conn.close()
server_socket.close()