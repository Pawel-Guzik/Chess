import pygame
from Figures import Pawn, Rook, Knight, Bishop, Queen, King, isMoveCorrect
# from Mechanics import clickNavi, highlightPossibleMoves
from Window import Window

pygame.init()
window = Window()

black_rooks = [Rook('black', 0, 0), Rook('black', 630, 0)]
black_knight = [Knight('black', 90, 0), Knight('black', 540, 0)]
black_bishop = [Bishop('black', 180, 0), Bishop('black', 450, 0)]
black_queen = Queen('black', 270, 0)
black_king = King('black', 360, 0)
black_pawns = [Pawn('black', x * 90, 90) for x in range(8)]

white_rooks = [Rook('white', 0, 630), Rook('white', 630, 630)]
white_knight = [Knight('white', 90, 630), Knight('white', 540, 630)]
white_bishop = [Bishop('white', 180, 630), Bishop('white', 450, 630)]
white_queen = Queen('white', 270, 630)
white_king = King('white', 360, 630)
white_pawns = [Pawn('white', x * 90, 540) for x in range(8)]


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


def moveFigure():
    global locations
    global move

    if board[locations['figure'][0]][locations['figure'][1]].color == 'white':
        move = 'black'
    else:
        move = 'white'

    if isinstance(board[locations['figure'][0]][locations['figure'][1]], Pawn):
        board[locations['figure'][0]][locations['figure'][1]].was_moving = True

    board[locations['figure'][0]][locations['figure'][1]].y = locations['field'][0] * 90
    board[locations['figure'][0]][locations['figure'][1]].x = locations['field'][1] * 90

    if board[locations['field'][0]][locations['field'][1]] != ' ':
        board[locations['field'][0]][locations['field'][1]] = ' '

    (board[locations['figure'][0]][locations['figure'][1]], board[locations['field'][0]][locations['field'][1]]) = (
        board[locations['field'][0]][locations['field'][1]], board[locations['figure'][0]][locations['figure'][1]])

    moveLoc = [locations['figure'], locations['field']]

    locations = {'figure': False, 'field': False}

    return moveLoc


run = True
move = 'white'
isDone = False
locations = {'figure': False, 'field': False}
possibleMoves = []
moveLoc = {}
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        click = pygame.mouse.get_pressed()[0]
        if click is True:
            clickLocation = clickNavi(pygame.mouse.get_pos())

            if board[clickLocation[0]][clickLocation[1]] != ' ':
                if board[clickLocation[0]][clickLocation[1]].color == move:
                    locations['figure'] = clickLocation
                    possibleMoves = board[locations['figure'][0]][locations['figure'][1]].isMovePossible(locations,board)
                    isMoveCorrect(board[locations['figure'][0]][locations['figure'][1]],possibleMoves, locations['figure'], board)

            if len(possibleMoves) > 0:
                for a in possibleMoves:
                    if a == clickLocation:
                        locations['field'] = clickLocation
                        moveLoc = moveFigure()

                        possibleMoves = []
                        black_king.check = black_king.isCheck(board, (int(black_king.y / 90), int(black_king.x / 90)))
                        white_king.check = white_king.isCheck(board, (int(white_king.y / 90), int(white_king.x / 90)))


    window.drawBoard(possibleMoves, board, locations, moveLoc)

    pygame.display.update()
