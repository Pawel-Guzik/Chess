import socket
from _thread import *

SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as e:
    str(e)


players = ['white', 'black']

move = ''
turn = 'white'
def thrededClient(conn, addr, player):
    global move, turn
    print(f'[NEW CONNECTION] {addr} connected')
    conn.send(str.encode(players[player]))

    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            else:
                if data == 'waiting':
                    print('someone"s is waiting')
                    print(move, ' <-- move')
                    if move == '':
                        reply = 'waiting'
                    else:
                        reply = move
                        move = ''
                elif data == 'white' or data == 'black':
                    reply = turn
                else:
                    if player == 0:
                        turn = 'black'
                    elif player == 1:
                        turn = 'white'
                    move = data
                    reply = data




                print("Received: ", data)
                print("Reply: ", reply)
            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    server.listen()

    conn, addr = server.accept()
    print("Connected to:", addr)

    start_new_thread(thrededClient, (conn, addr, currentPlayer))
    currentPlayer += 1