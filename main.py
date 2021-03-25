import pygame
from Figures import Pawn, Rook, Knight, Bishop, Queen, King, isMoveCorrect, castlingMove
from player import Player
from network import Network
from Window import Window
from time import sleep
import threading

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
def choseFigure(click):

    if 720 <= click[0] < 810:
        if 270 <= click[1] < 310:
            print('queen')
            return True
        elif 310 <= click[1] < 400:
            print('knight')
            return True
    elif 810 <= click[0] < 900:
        if 270 <= click[1] < 310:
            print('rook')
            return True
        elif 310 <= click[1] < 400:
            print('bishop')
            return True
    return False
def decodeTime(strTime):
    times = strTime.split()
    return int(times[0]), int(times[1])


def decodeMove(strMove):
    if strMove == 'waiting':
        return 'waiting'
    figLoc = (int(strMove[2]), int(strMove[5]))
    fieldLoc = (int(strMove[10]), int(strMove[13]))
    return figLoc, fieldLoc


def encodeMove(locations):
    figLoc = locations['figure']
    fieldLoc = locations['field']
    strMove = str((figLoc, fieldLoc))
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


def isPromotion(figLoc, fieldLoc):
    fig = type(board[figLoc[0]][figLoc[1]])
    if fig == Pawn and board[figLoc[0]][figLoc[1]].color == 'white' and fieldLoc[0] == 0:
        return True
    elif fig == Pawn and board[figLoc[0]][figLoc[1]].color == 'black' and fieldLoc[0] == 7:
        return True
    return False


def moveFigure(figLoc, fieldLoc):
    fig = type(board[figLoc[0]][figLoc[1]])
    # castling
    if type(board[figLoc[0]][figLoc[1]]) == King and (figLoc[1] - fieldLoc[1] == 2 or fieldLoc[1] - figLoc[1] == 2):

        if figLoc[1] - fieldLoc[1] == 2:
            castlingMove(board, figLoc, fieldLoc, (0, 3))

        elif fieldLoc[1] - figLoc[1] == 2:
            castlingMove(board, figLoc, fieldLoc, (7, 5))

        moveLoc = [figLoc, fieldLoc]

        return moveLoc

    if fig == Pawn or fig == King or fig == Rook:
        board[figLoc[0]][figLoc[1]].was_moving = True

    board[figLoc[0]][figLoc[1]].y = fieldLoc[0] * 90
    board[figLoc[0]][figLoc[1]].x = fieldLoc[1] * 90

    if board[fieldLoc[0]][fieldLoc[1]] != ' ':
        board[fieldLoc[0]][fieldLoc[1]] = ' '

    (board[figLoc[0]][figLoc[1]], board[fieldLoc[0]][fieldLoc[1]]) = (
    board[fieldLoc[0]][fieldLoc[1]], board[figLoc[0]][figLoc[1]])

    moveLoc = [figLoc, fieldLoc]

    return moveLoc


def isPromotion (figLoc, fieldLoc):
    fig = type(board[figLoc[0]][figLoc[1]])
    if fig == Pawn and board[figLoc[0]][figLoc[1]].color == 'white' and fieldLoc[0] == 0:
        return True
    elif fig == Pawn and board[figLoc[0]][figLoc[1]].color == 'black' and fieldLoc[0] == 7:
        return True
    return False


move = 'white'
promotion = 'no promotion'


# def choosePromoFigure(click)


def menu():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = pygame.mouse.get_pos()

                if 300 <= click[0] <= 600:
                    if 285 <= click[1] <= 435:
                        game()

        window.menuScreen()


def game():
    run = True
    global move
    locations = {'figure': False, 'field': False}
    possibleMoves = []
    moveLoc = {}
    global promotion
    clock = pygame.time.Clock()
    network = Network()
    opponentColor = ''
    promotion = False
    p1 = Player(network.color)
    x = lambda a: True if a == 'True' else False
    isOpponent = x(network.send('ready'))

    while not isOpponent:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.waitingForPlayer()
        isOpponent = x(network.send('ready'))
    if network.color == 'white':
        opponentColor = 'black'
    if network.color == 'black':
        opponentColor = 'white'
    p2 = Player(opponentColor)

    print("Player ", p1.color)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if p1.color == move:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click = pygame.mouse.get_pos()
                    clickLocation = clickNavi(click)

                    if board[clickLocation[0]][clickLocation[1]] != ' ':
                        if board[clickLocation[0]][clickLocation[1]].color == move:
                            locations['figure'] = clickLocation
                            possibleMoves = board[locations['figure'][0]][locations['figure'][1]].possibleMoves(
                                locations, board)
                            isMoveCorrect(possibleMoves, locations['figure'], board)

                    if len(possibleMoves) > 0:
                        for a in possibleMoves:
                            if a == clickLocation:
                                locations['field'] = clickLocation
                                promotion = isPromotion(locations['figure'], locations['field'])
                                while promotion:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            click = pygame.mouse.get_pos()
                                            promotion = not choseFigure(click)

                                    pTimes = decodeTime(network.send('pTimes'))
                                    window.drawBoard(possibleMoves, board, locations, moveLoc, pTimes, move, promotion)
                                network.send(encodeMove(locations))
                                possibleMoves = []
                                black_king.check = black_king.isCheck(board,
                                                                      (int(black_king.y / 90), int(black_king.x / 90)))
                                white_king.check = white_king.isCheck(board,
                                                                      (int(white_king.y / 90), int(white_king.x / 90)))

        ruch = decodeMove(network.send('waiting'))

        if ruch != 'waiting':
            locations['figure'], locations['field'] = ruch

        if locations['figure'] and locations['field']:
            moveLoc = moveFigure(locations['figure'], locations['field'])
            locations = {'figure': False, 'field': False}
            if move == 'white':
                move = 'black'
            else:
                move = 'white'

        black_king.isCheckMate(board)
        white_king.isCheckMate(board)
        pTimes = decodeTime(network.send('pTimes'))
        window.drawBoard(possibleMoves, board, locations, moveLoc, pTimes)


menu()
# game()
