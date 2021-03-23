import socket
from _thread import *
from time import sleep
import pickle
SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as e:
    str(e)




def timer(player):
    global turn, players, pTimes
    seconds = 10*60
    while seconds > 0:
        if players[player] == turn:
            pTimes[player] -= 1
            sleep(1)

currentPlayer = 0
pTimes = [600, 600]
players = ['white', 'black']
was_moving = []
move = ''
turn = 'white'

def encodeTime(times):
    return str(times[0]) + ' ' + str(times[1])


def thrededClient(conn, addr, player):
    global move, turn, was_moving
    print(f'[NEW CONNECTION] {addr} connected')
    conn.send(str.encode(players[player]))
    start_new_thread(timer, (player,))

    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            else:
                if data == 'waiting':
                    if move == '':
                        reply = 'waiting'
                    else:

                        if player in was_moving:
                            reply = 'waiting'
                        else:
                            was_moving.append(player)
                            reply = move
                elif data == 'pTimes':
                    reply = encodeTime(pTimes)
                else:
                    print(data)
                    move = data
                    reply = "got"

                if len(was_moving) == 2:
                    move = ''
                    was_moving = []
                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'

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