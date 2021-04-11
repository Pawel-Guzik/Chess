import socket
from _thread import *
from time import sleep
from gui import db
from game import Game
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


# pTimes = [600, 600]
# players = ['white', 'black']
# was_moving = []
# move = ''
# turn = 'white'
# isPromotion = False
# promoFigure = ' '
# asked = []
# nicknames = []
# winner = ''


# def encodeTime(times):
#     return str(times[0]) + ' ' + str(times[1])


def writeResultTodatabase(winner, nicknames):
    mycursor = db.cursor()
    values = (nicknames[0], nicknames[1], nicknames[winner])
    mycursor.execute("INSERT INTO game_history (P1_nick, P2_nick, winner) VALUES (%s,%s,%s)",values)
    db.commit()
    mycursor.execute("SELECT nickname, points FROM user WHERE nickname IN (%s, %s)", (nicknames[0], nicknames[1]))
    records = mycursor.fetchall()
    for x in records:
        points = x[1]
        if x[0] == nicknames[winner]:
            points += 9
        else:
            points -= 9
            print(x[0], points)
        mycursor.execute("UPDATE user SET points = %s WHERE nickname = %s", (points, x[0]))
        db.commit()

def thrededClient(conn, addr, player, gameId):
    # global move, turn, was_moving, currentPlayer, isPromotion, promoFigure, asked, nicknames, winner
    global games
    print(f'[NEW CONNECTION] {addr} connected')
    conn.send(str.encode(games[gameId].players[player]))


    while True:
        try:
            data = conn.recv(2048).decode()
            print(data)
            if not data:
                print("Disconnected")
                break
            else:
                if data == 'waiting':
                    if games[gameId].move == '':
                        reply = 'waiting'
                    else:

                        if player in games[gameId].was_moving:
                            reply = 'waiting'
                        else:
                            games[gameId].was_moving.append(player)
                            reply = games[gameId].move

                elif data == 'pTimes':
                    reply = games[gameId].encodeTime()
                elif data == 'ready':
                    print(player)
                    if games[gameId].areTwoPlayers == True:
                        reply = 'True'
                        start_new_thread(games[gameId].timer, (player,))
                    else:
                        reply = 'False'
                elif data == 'queen' or data == 'knight' or data == 'rook' or data == 'bishop':
                    games[gameId].promoFigure = data
                    reply = data

                elif data == 'is promotion':
                    reply = games[gameId].promoFigure

                elif data == 'promoted':
                    games[gameId].asked.append(player)
                    if len(games[gameId].asked) == 2:
                        games[gameId].promoFigure = ' '
                        games[gameId].asked = []

                elif data == 'nicknames':
                    reply = str(games[gameId].nicknames[0]) + ' ' + str(games[gameId].nicknames[1])

                elif 'nickname' in data:
                    tab = data.split()
                    games[gameId].nicknames.append(tab[1])
                    reply = 'ok'

                elif data == 'white won':
                    if games[gameId].winner == '':
                        games[gameId].winner = 0
                        writeResultTodatabase(games[gameId].winner, games[gameId].nicknames)
                elif data == 'black won':
                    if games[gameId].winner == '':
                        games[gameId].winner = 1
                        writeResultTodatabase(games[gameId].winner,games[gameId].nicknames)

                else:
                    games[gameId].move = data
                    reply = "got"

                if len(games[gameId].was_moving) == 2:
                    games[gameId].move = ''
                    games[gameId].was_moving = []
                    if games[gameId].turn == 'white':
                        games[gameId].turn = 'black'
                    else:
                        games[gameId].turn = 'white'

            conn.sendall(str.encode(reply))
        except:
            break

    print("Lost connection")
    conn.close()



games = {}
idCounter = 0
while True:
    server.listen()
    idCounter += 1
    conn, addr = server.accept()
    gameId = int((idCounter - 1)/2)

    if idCounter % 2 == 1:
        player = 0
        games[gameId] = Game(gameId)
    else:
        player = 1
        games[gameId].areTwoPlayers = True


    start_new_thread(thrededClient, (conn, addr, player, gameId))