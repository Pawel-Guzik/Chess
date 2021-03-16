import socket
from _thread import *
from Figures import Rook, Knight, Bishop, Queen, King, Pawn
import pickle





black_rooks = [Rook('black', 0, 0, 'img/C_Wieza.png'), Rook('black', 630, 0, 'img/C_Wieza.png')]
black_knight = [Knight('black', 90, 0, 'img/C_Kon.png'), Knight('black', 540, 0, 'img/C_Kon.png')]
black_bishop = [Bishop('black', 180, 0, 'img/C_Goniec.png'), Bishop('black', 450, 0, 'img/C_Goniec.png')]
black_queen = Queen('black', 270, 0, 'img/C_Dama.png')
black_king = King('black', 360, 0, 'img/C_Krol.png')
black_pawns = [Pawn('black', x * 90, 90, 'img/C_Pion.png') for x in range(8)]


white_rooks = [Rook('white', 0, 630, 'img/B_Wieza.png'), Rook('white', 630, 630, 'img/B_Wieza.png')]
white_knight = [Knight('white', 90, 630, 'img/B_Kon.png'), Knight('white', 540, 630, 'img/B_Kon.png')]
white_bishop = [Bishop('white', 180, 630, 'img/B_Goniec.png'), Bishop('white', 450, 630, 'img/B_Goniec.png')]
white_queen = Queen('white', 270, 630, 'img/B_Dama.png')
white_king = King('white', 360, 630, 'img/B_Krol.png')
white_pawns = [Pawn('white', x * 90, 540, 'img/B_Pion.png') for x in range(8)]

board = [
    [black_rooks[0], black_knight[0], black_bishop[0], black_queen, black_king, black_bishop[1], black_knight[1],
     black_rooks[1]],
    black_pawns,
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    white_pawns,
    [white_rooks[0], white_knight[0], white_bishop[0], white_queen, white_king, white_bishop[1], white_knight[1],
     white_rooks[1]]
]






SERVER = socket.gethostbyname(socket.gethostname())
PORT = 5555
ADDR = (SERVER, PORT)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind(ADDR)
except socket.error as e:
    str(e)


players = ['white', 'black']

def thrededClient(conn, addr, player):
    print(f'[NEW CONNECTION] {addr} connected')
    conn.send(str.encode(players[player]))

    while True:
        try:
            data = conn.recv(2048).decode()

            if not data:
                print("Disconnected")
                break
            else:
                reply = data
                pass
                print("Received: ", data)
            conn.sendall(str.encode(data))
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