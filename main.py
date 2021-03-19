import pygame
from Figures import Pawn, Rook, Knight, Bishop, Queen, King, Figure, isMoveCorrect, castlingMove
# from Mechanics import clickNavi, highlightPossibleMoves
from player import Player
from network import Network

from Window import Window

pygame.init()
window = Window()

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



def decodeMove(strMove):
    print(strMove)
    if strMove == 'white' or strMove == 'black':
        return 'waiting'
    print(type(strMove))
    figLoc = (int(strMove[2]), int(strMove[5]))
    fieldLoc = (int(strMove[10]), int(strMove[13]))

    return figLoc, fieldLoc

def encodeMove(locations):
    figLoc = locations['figure']
    fieldLoc = locations['field']

    strMove = str((figLoc, fieldLoc))
    print(strMove)
    return strMove



def clickNavi(mouseposition):
    x = y = 0
    for a in range(8):
        if mouseposition[0] >= a * 90 and mouseposition[0] < a * 90 + 90:
            x = a
            break
    for a in range(8):
        if mouseposition[1] >= a * 90 and mouseposition[1] < a * 90 + 90:
            y = a
            break
    return y, x


def moveFigure(figLoc, fieldLoc):
    global move

    # if board[figLoc[0]][figLoc[1]].color == 'white':
    #     move = 'black'
    #     # network.send('bialy sie ruszyl')
    # else:
    #     move = 'white'
    #     # network.send('czarny sie ruszyl')

    # castling
    if type(board[figLoc[0]][figLoc[1]]) == King and (figLoc[1] - fieldLoc[1] == 2 or fieldLoc[1] - figLoc[1] == 2):
        if figLoc[1] - fieldLoc[1] == 2:
            castlingMove(board, figLoc, fieldLoc, (0, 3))
        elif fieldLoc[1] - figLoc[1] == 2:
            castlingMove(board, figLoc, fieldLoc, (7, 5))

        moveLoc = [figLoc, fieldLoc]

        return moveLoc

    fig = type(board[figLoc[0]][figLoc[1]])

    if fig == Pawn or fig == King or fig == Rook:
        board[figLoc[0]][figLoc[1]].was_moving = True

    board[figLoc[0]][figLoc[1]].y = fieldLoc[0] * 90
    board[figLoc[0]][figLoc[1]].x = fieldLoc[1] * 90

    if board[fieldLoc[0]][fieldLoc[1]] != ' ':
        board[fieldLoc[0]][fieldLoc[1]] = ' '

    (board[figLoc[0]][figLoc[1]], board[fieldLoc[0]][fieldLoc[1]]) = (board[fieldLoc[0]][fieldLoc[1]], board[figLoc[0]][figLoc[1]])

    moveLoc = [figLoc, fieldLoc]

    return moveLoc


run = True
move = 'white'
isDone = False
locations = {'figure': False, 'field': False}
possibleMoves = []
moveLoc = {}
clock = pygame.time.Clock()
network = Network()
opponentColor = ''
p1 = Player(network.color)
if network.color == 'white':
    opponentColor = 'black'
if network.color == 'black':
    opponentColor = 'white'
p2 = Player(opponentColor)

# print(p1.color)

while run:
    clock.tick(60)
    # print(move)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if p1.color == move:
            click = pygame.mouse.get_pressed()[0]
            if click is True:
                clickLocation = clickNavi(pygame.mouse.get_pos())

                if board[clickLocation[0]][clickLocation[1]] != ' ':
                    if board[clickLocation[0]][clickLocation[1]].color == move:
                        locations['figure'] = clickLocation
                        possibleMoves = board[locations['figure'][0]][locations['figure'][1]].possibleMoves(locations,board)
                        isMoveCorrect(possibleMoves, locations['figure'], board)

                if len(possibleMoves) > 0:
                    for a in possibleMoves:
                        if a == clickLocation:
                            locations['field'] = clickLocation
                            # network.send(encodeMove(locations))
                            locations['figure'], locations['field'] = decodeMove(network.send(encodeMove(locations)))
                            moveLoc = moveFigure(locations['figure'], locations['field'])
                            locations = {'figure': False, 'field': False}

                            possibleMoves = []
                            black_king.check = black_king.isCheck(board, (int(black_king.y / 90), int(black_king.x / 90)))
                            white_king.check = white_king.isCheck(board, (int(white_king.y / 90), int(white_king.x / 90)))
                            black_king.isCheckMate(board)
                            white_king.isCheckMate(board)

    if p1.color != move:
        try:
            get = network.send('waiting')
            print(get)
            if get != 'waiting':
                locations['figure'], locations['field'] = decodeMove(get)
                moveLoc = moveFigure(locations['figure'], locations['field'])
                print(move)
        except:
            pass

    move = network.send(move)

    window.drawBoard(possibleMoves, board, locations, moveLoc)
    pygame.display.update()

