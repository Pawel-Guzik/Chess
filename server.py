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
isPromotion = False
promoFigure = ' '
asked = []
def encodeTime(times):
    return str(times[0]) + ' ' + str(times[1])


def thrededClient(conn, addr, player):
    global move, turn, was_moving, currentPlayer, isPromotion, promoFigure, asked
    print(f'[NEW CONNECTION] {addr} connected')
    conn.send(str.encode(players[player]))


    while True:
        try:
            data = conn.recv(2048).decode()
            print(data)
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
                elif data == 'ready':
                    print(currentPlayer)
                    if currentPlayer == 2:
                        reply = 'True'
                        start_new_thread(timer, (player,))
                    else:
                        reply = 'False'
                elif data == 'queen' or data == 'knight' or data == 'rook' or data == 'bishop':
                    promoFigure = data
                    reply = data

                elif data == 'is promotion':
                    # if len(asked) == 2:
                    #     promoFigure = ' '
                    #     asked = []
                    # asked.append(player)
                    reply = promoFigure
                elif data == 'promoted':
                    asked.append(player)
                    if len(asked) == 2:
                        promoFigure = ' '
                        asked = []

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



while True:
    server.listen()

    conn, addr = server.accept()
    print("Connected to:", addr)

    start_new_thread(thrededClient, (conn, addr, currentPlayer))
    currentPlayer += 1