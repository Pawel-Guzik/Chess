import pygame
from Figures import Pawn, Rook, Knight, Bishop, Queen, King, isMoveCorrect, castlingMove
from player import Player
from network import Network
from Window import Window
from gui import Gui



pygame.init()
# window = Window()

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


def choseFigure(click, network):

    if 720 <= click[0] < 810:
        if 270 <= click[1] < 360:
            network.send('queen')
            return True
        elif 360 <= click[1] < 450:
            network.send('knight')
            return True
    elif 810 <= click[0] < 900:
        if 270 <= click[1] < 360:
            network.send('rook')
            return True
        elif 360 <= click[1] < 450:
            network.send('bishop')
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
    isMoving = board[figLoc[0]][figLoc[1]].color
    if fig == Pawn:
        if fieldLoc[0] - figLoc[0] == 2 or fieldLoc[0] - figLoc[0] == -2:
            board[figLoc[0]][figLoc[1]].enPassant = True
        else:
            board[figLoc[0]][figLoc[1]].enPassant = False
        print(board[figLoc[0]][figLoc[1]].enPassant)

    # castling
    if fig == King and (figLoc[1] - fieldLoc[1] == 2 or fieldLoc[1] - figLoc[1] == 2):

        if figLoc[1] - fieldLoc[1] == 2:
            castlingMove(board, figLoc, fieldLoc, (0, 3))

        elif fieldLoc[1] - figLoc[1] == 2:
            castlingMove(board, figLoc, fieldLoc, (7, 5))

        moveLoc = [figLoc, fieldLoc]
        Pawn.resetEnPassant(isMoving, board)
        return moveLoc


    # en passant move
    if fig == Pawn and board[fieldLoc[0]][fieldLoc[1]] == ' ':
        if fieldLoc[1] - figLoc[1] == 1 or figLoc[1] - fieldLoc[1] == 1:
            if isMoving == 'white':
                board[fieldLoc[0] + 1][fieldLoc[1]] = ' '
            elif isMoving == 'black':
                board[fieldLoc[0] - 1][fieldLoc[1]] = ' '

    if fig == Pawn or fig == King or fig == Rook:
        board[figLoc[0]][figLoc[1]].was_moving = True

    board[figLoc[0]][figLoc[1]].imgLoc = fieldLoc

    if board[fieldLoc[0]][fieldLoc[1]] != ' ':
        board[fieldLoc[0]][fieldLoc[1]] = ' '

    (board[figLoc[0]][figLoc[1]], board[fieldLoc[0]][fieldLoc[1]]) = (board[fieldLoc[0]][fieldLoc[1]], board[figLoc[0]][figLoc[1]])

    moveLoc = [figLoc, fieldLoc]
    Pawn.resetEnPassant(isMoving, board)
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

def promotPawn(fieldLoc, promo_figure, move):
    if move == 'white':
        c = 'B_'
    elif move == 'black':
        c = 'C_'
    if promo_figure == 'queen':
        board[fieldLoc[0]][fieldLoc[1]] = Queen(move, fieldLoc[1]*90, fieldLoc[0]*90, f'img/{c}Dama.png')
    elif promo_figure == 'bishop':
        board[fieldLoc[0]][fieldLoc[1]] = Bishop(move, fieldLoc[1]*90, fieldLoc[0]*90, f'img/{c}Goniec.png')
    elif promo_figure == 'knight':
        board[fieldLoc[0]][fieldLoc[1]] = Knight(move, fieldLoc[1]*90, fieldLoc[0]*90, f'img/{c}Kon.png')
    elif promo_figure == 'rook':
        board[fieldLoc[0]][fieldLoc[1]] = Rook(move, fieldLoc[1]*90, fieldLoc[0]*90, f'img/{c}Wieza.png')


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
                        print('jestem')
                        run = False
            if run:
                window.menuScreen()


def game():
    global nickname, move, promotion
    promotion = False
    run = True
    locations = {'figure': False, 'field': False}
    change_move = {'white': 'black', 'black': 'white'}
    possibleMoves = []
    nicknames = []
    moveLoc = {}

    clock = pygame.time.Clock()
    network = Network()
    p1 = Player(network.color)
    network.send(f'nickname {nickname}')
    x = lambda a: True if a == 'True' else False
    isOpponent = x(network.send('ready'))

    # waiting for second player to connect
    while not isOpponent:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        window.waitingForPlayer()
        isOpponent = x(network.send('ready'))


    print("Player ", p1.color)

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
                                #Pawn promotion
                                while promotion:
                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            run = False
                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            click = pygame.mouse.get_pos()
                                            promotion = not choseFigure(click, network)

                                    pTimes = decodeTime(network.send('pTimes'))
                                    window.drawBoard(possibleMoves, board, locations, moveLoc, pTimes, nicknames, move, promotion)
                                network.send(encodeMove(locations))
                                possibleMoves = []
                                black_king.check = black_king.isCheck(board,
                                                                      (int(black_king.y / 90), int(black_king.x / 90)))
                                white_king.check = white_king.isCheck(board,
                                                                      (int(white_king.y / 90), int(white_king.x / 90)))
        is_promotion = network.send('is promotion')
        ruch = decodeMove(network.send('waiting'))

        if ruch != 'waiting':
            locations['figure'], locations['field'] = ruch

        if locations['figure'] and locations['field']:
            moveLoc = moveFigure(locations['figure'], locations['field'])
            print(is_promotion)
            if is_promotion != ' ':
                promotPawn(locations['field'], is_promotion, move)
                network.send('promoted')
            locations = {'figure': False, 'field': False}
            move = change_move[move]

        if black_king.isCheckMate(board):
            network.send('white won')
            print('białe wygrały koniec gry')
            pygame.quit()
            break
        if white_king.isCheckMate(board):
            network.send('black won')
            print('czarne wygrały koniec gry')
            pygame.quit()
            break

        if nicknames == []:
            nicknames = network.send('nicknames')
            print(nicknames)

        pTimes = decodeTime(network.send('pTimes'))
        window.drawBoard(possibleMoves, board, locations, moveLoc, pTimes, nicknames)

welcomeWindow = Gui()
welcomeWindow.place(relx=.5, rely=.5, anchor="center")
loop_active = True
isWindowVisible = True

while loop_active:
    welcomeWindow.root.update()

    if welcomeWindow.startGame:
        nickname = welcomeWindow.loggedUser
        print(nickname)
        window = Window()
        menu()
        welcomeWindow.startGame = False

    elif welcomeWindow.visible == False:
        welcomeWindow.visible = True
        welcomeWindow.root.deiconify()
