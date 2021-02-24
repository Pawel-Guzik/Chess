import pygame
from Figures import Pawn, Rook, Knight, Bishop, Queen, King

pygame.init()

window = pygame.display.set_mode((720, 720))

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

print(black_pawns[2])

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



def highlightPossibleMoves(moves):
    for x, y in moves:
        if board[x][y] != ' ':
            pass
        else:
            pygame.draw.circle(window, (0, 0, 0), (y * 90 + 45, x * 90 + 45), 15)




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

    locations = {'figure': False, 'field': False}


def redrawBoard(moves):
    squareSize = 90



    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:
                pygame.draw.rect(window, (200, 200, 200), (i * squareSize, j * squareSize, squareSize, squareSize))
            else:
                pygame.draw.rect(window, (50, 50, 50), (i * squareSize, j * squareSize, squareSize, squareSize))

    for a, line in enumerate(board):
        for b, column in enumerate(line):
            if board[a][b] != ' ':
                window.blit(board[a][b].img, (board[a][b].x, board[a][b].y))

    highlightPossibleMoves(moves)


run = True
move = 'white'
isDone = False
locations = {'figure': False, 'field': False}


possibleMoves = []

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
                    possibleMoves = board[locations['figure'][0]][locations['figure'][1]].isMovePossible(locations,
                                                                                                         board)


            if len(possibleMoves) > 0:
                for a in possibleMoves:
                    if a == clickLocation:
                        locations['field'] = clickLocation
                        moveFigure()
                        print('Współrzędne króla', int(black_king.y/90), int(black_king.x/90))
                        print(black_king.isCheck(board, (int(black_king.y/90), int(black_king.x/90))))
                        possibleMoves = []

    redrawBoard(possibleMoves)

    pygame.display.update()
