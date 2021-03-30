import pygame


class Figure:
    """
    Parent Class for all figures
    """

    def __init__(self, color, x, y, img):
        self.color = color
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        if self.color == 'black':
            self.colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            self.colors = {'friendly': 'white', 'opponent': 'black'}

    def __str__(self):
        return f'{self.color} {type(self).__name__} ({self.x},{self.y})'

    def checkLongMoves(self, board, possibleMoves, row, column):
        if board[row][column] == ' ':
            possibleMoves.append((row, column))
        else:
            if board[row][column].color == self.colors['friendly']:
                return False
            if board[row][column].color == self.colors['opponent']:
                possibleMoves.append((row, column))
                return False
        return True

    def checkShortMove(self, board, possibleMoves, row, column):
        if board[row][column] == ' ':
            possibleMoves.append((row, column))
        else:
            if board[row][column].color == self.colors['opponent']:
                possibleMoves.append((row, column))

class Pawn(Figure):

    def __init__(self, color, x, y, img):
        super().__init__(color, x, y, img)
        self.was_moving = False
        self.enPassant = False

    def checkMove(self, board):
        pass

    def possibleMoves(self, locations, board):
        pawnLoc = locations['figure']
        possibleMoves = []

        if self.color == 'white':

            if pawnLoc[0] > 0:
                # ruch do przodu
                if board[pawnLoc[0] - 1][pawnLoc[1]] == ' ':
                    possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1]))

                # zbicie w prawo
                if pawnLoc[1] < 7:
                    if board[pawnLoc[0] - 1][pawnLoc[1] + 1] != ' ' and board[pawnLoc[0] - 1][pawnLoc[1] + 1].color == 'black':
                        possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1] + 1))
                    # en passant
                    if type(board[pawnLoc[0]][pawnLoc[1] + 1]) == Pawn:
                        if board[pawnLoc[0]][pawnLoc[1] + 1].color == 'black' and board[pawnLoc[0] - 1][pawnLoc[1] + 1] == ' ' and board[pawnLoc[0]][pawnLoc[1] + 1].enPassant:
                            possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1] + 1))

                # zbicie w lewo
                if pawnLoc[1] > 0:
                    if board[pawnLoc[0] - 1][pawnLoc[1] - 1] != ' ' and board[pawnLoc[0] - 1][pawnLoc[1] - 1].color == 'black':
                        possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1] - 1))

                    if type(board[pawnLoc[0]][pawnLoc[1] - 1]) == Pawn:
                        if board[pawnLoc[0]][pawnLoc[1] - 1].color == 'black' and board[pawnLoc[0] - 1][pawnLoc[1] - 1] == ' ' and board[pawnLoc[0]][pawnLoc[1] - 1].enPassant:
                            possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1] - 1))


                # ruch o dwa do przodu
                if self.was_moving is False and board[pawnLoc[0] - 1][pawnLoc[1]] == ' ' and board[pawnLoc[0] - 2][
                    pawnLoc[1]] == ' ':
                    possibleMoves.append((pawnLoc[0] - 2, pawnLoc[1]))



        if self.color == 'black':
            # ruch do przodu
            if pawnLoc[0] < 7:
                if board[pawnLoc[0] + 1][pawnLoc[1]] == ' ':
                    possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1]))

                # zbicie w prawo
                if pawnLoc[1] < 7:
                    if board[pawnLoc[0] + 1][pawnLoc[1] + 1] != ' ' and board[pawnLoc[0] + 1][pawnLoc[1] + 1].color == 'white':
                        possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1] + 1))

                    if type(board[pawnLoc[0]][pawnLoc[1] + 1]) == Pawn:
                        if board[pawnLoc[0]][pawnLoc[1] + 1].color == 'white' and board[pawnLoc[0] + 1][pawnLoc[1] + 1] == ' ' and board[pawnLoc[0]][pawnLoc[1] + 1].enPassant:
                            possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1] + 1))

                # zbicie w lewo
                if pawnLoc[1] > 0:
                    if board[pawnLoc[0] + 1][pawnLoc[1] - 1] != ' ' and board[pawnLoc[0] + 1][pawnLoc[1] - 1].color == 'white':
                        possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1] - 1))

                    if type(board[pawnLoc[0]][pawnLoc[1] - 1]) == Pawn:
                        if board[pawnLoc[0]][pawnLoc[1] - 1].color == 'white' and board[pawnLoc[0] + 1][pawnLoc[1] - 1] == ' ' and board[pawnLoc[0]][pawnLoc[1] - 1].enPassant:
                            possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1] - 1))

            if self.was_moving is False and board[pawnLoc[0] + 1][pawnLoc[1]] == ' ' and board[pawnLoc[0] + 2][pawnLoc[1]] == ' ':
                possibleMoves.append((pawnLoc[0] + 2, pawnLoc[1]))




        return possibleMoves


    @staticmethod
    def resetEnPassant(move, board):
        # reset = 'white'
        if move == 'white':
            reset = 'black'
        elif move == 'black':
            reset = 'white'

        for a, row in enumerate(board):
            for b, column in enumerate(row):
                if type(board[a][b]) == Pawn:
                    if board[a][b].color == reset:
                        board[a][b].enPassant = False


class Knight(Figure):

    def __init__(self, color, x, y, img):
        super().__init__(color, x, y, img)

    def possibleMoves(self, locations, board):
        knightLoc = locations['figure']
        possibleMoves = []

        # left - down moves
        if knightLoc[0] < 7 and knightLoc[1] > 1:
            super().checkShortMove(board, possibleMoves, knightLoc[0] + 1, knightLoc[1] - 2)

        if knightLoc[0] < 6 and knightLoc[1] > 0:
            super().checkShortMove(board, possibleMoves, knightLoc[0] + 2, knightLoc[1] - 1)

        # right - down moves
        if knightLoc[0] < 7 and knightLoc[1] < 6:
            super().checkShortMove(board, possibleMoves, knightLoc[0] + 1, knightLoc[1] + 2)

        if knightLoc[0] < 6 and knightLoc[1] < 7:
            super().checkShortMove(board, possibleMoves, knightLoc[0] + 2, knightLoc[1] + 1)

        # right - up moves
        if knightLoc[0] > 0 and knightLoc[1] < 6:
            super().checkShortMove(board, possibleMoves, knightLoc[0] - 1, knightLoc[1] + 2)

        if knightLoc[0] > 1 and knightLoc[1] < 7:
            super().checkShortMove(board, possibleMoves, knightLoc[0] - 2, knightLoc[1] + 1)

        # left - up moves
        if knightLoc[0] > 0 and knightLoc[1] > 1:
            super().checkShortMove(board, possibleMoves, knightLoc[0] - 1, knightLoc[1] - 2)

        if knightLoc[0] > 1 and knightLoc[1] > 0:
            super().checkShortMove(board, possibleMoves, knightLoc[0] - 2, knightLoc[1] - 1)

        return possibleMoves


class Bishop(Figure):

    def __init__(self, color, x, y, img):
        super().__init__(color, x, y, img)

    def possibleMoves(self, locations, board):
        bishopLoc = locations['figure']
        possibleMoves = []

        # left - down moves
        if bishopLoc[0] < 7 and bishopLoc[1] > 0:
            for i in range(1, 8):
                if bishopLoc[0] + i > 7 or bishopLoc[1] - i < 0:
                    break
                if super().checkLongMoves(board, possibleMoves, bishopLoc[0] + i, bishopLoc[1] - i) is False:
                    break

        # left - up moves
        if bishopLoc[0] > 0 and bishopLoc[1] > 0:
            for i in range(1, 8):
                if bishopLoc[0] - i < 0 or bishopLoc[1] - i < 0:
                    break
                if super().checkLongMoves(board, possibleMoves, bishopLoc[0] - i, bishopLoc[1] - i) is False:
                    break

        # right - down moves
        if bishopLoc[0] < 7 and bishopLoc[1] < 7:
            for i in range(1, 8):
                if bishopLoc[0] + i > 7 or bishopLoc[1] + i > 7:
                    break
                if super().checkLongMoves(board, possibleMoves, bishopLoc[0] + i, bishopLoc[1] + i) is False:
                    break

        # right - up moves
        if bishopLoc[0] > 0 and bishopLoc[1] < 7:
            for i in range(1, 8):
                if bishopLoc[0] - i < 0 or bishopLoc[1] + i > 7:
                    break
                if super().checkLongMoves(board, possibleMoves, bishopLoc[0] - i, bishopLoc[1] + i) is False:
                    break

        return possibleMoves


class Rook(Figure):

    def __init__(self, color, x, y, img):
        super().__init__(color, x, y, img)
        self.was_moving = False


    def possibleMoves(self, locations, board):
        rookLoc = locations['figure']
        possibleMoves = []

        # down moves
        if rookLoc[0] < 7:
            for a in range(1, 8):
                if rookLoc[0] + a == 8:
                    break
                if super().checkLongMoves(board, possibleMoves, rookLoc[0] + a, rookLoc[1]) is False:
                    break

        # up moves
        if rookLoc[0] > 0:
            for a in range(1, 8):
                if rookLoc[0] - a == 8:
                    break
                if super().checkLongMoves(board, possibleMoves, rookLoc[0] - a, rookLoc[1]) is False:
                    break

        # right moves
        if rookLoc[1] < 7:
            for a in range(1, 8):
                if rookLoc[1] + a == 8:
                    break
                if super().checkLongMoves(board, possibleMoves, rookLoc[0], rookLoc[1] + a) is False:
                    break

        # left moves
        if rookLoc[1] > 0:
            for a in range(1, 8):
                if rookLoc[1] - a == 8:
                    break
                if super().checkLongMoves(board, possibleMoves, rookLoc[0], rookLoc[1] - a) is False:
                    break
        return possibleMoves


class Queen(Rook, Bishop):

    def __init__(self, color, x, y, img):
        Bishop.__init__(self, color, x, y, img)

    def possibleMoves(self, locations, board):
        rookMoves = Rook.possibleMoves(self, locations, board)
        bishopMoves = Bishop.possibleMoves(self, locations, board)
        possibleMoves = rookMoves + bishopMoves
        # print(possibleMoves)
        return possibleMoves


class King(Figure):

    def __init__(self, color, x, y, img):
        super().__init__(color, x, y, img)
        self.check = False
        self.was_moving = False

    def possibleMoves(self, locations, board):
        possibleMoves = []
        kingLoc = locations['figure']

        # up move
        if kingLoc[0] > 0:
            super().checkShortMove(board, possibleMoves, kingLoc[0] - 1, kingLoc[1])

            # left - up move
            if kingLoc[1] > 0:
                super().checkShortMove(board, possibleMoves, kingLoc[0] - 1, kingLoc[1] - 1)

            # right - up move
            if kingLoc[1] < 7:
                super().checkShortMove(board, possibleMoves, kingLoc[0] - 1, kingLoc[1] + 1)

        # down move
        if kingLoc[0] < 7:
            super().checkShortMove(board, possibleMoves, kingLoc[0] + 1, kingLoc[1])

            # right - down move
            if kingLoc[1] < 7:
                super().checkShortMove(board, possibleMoves, kingLoc[0] + 1, kingLoc[1] + 1)

            # left - down move
            if kingLoc[1] > 0:
                super().checkShortMove(board, possibleMoves, kingLoc[0] + 1, kingLoc[1] - 1)

        # right move
        if kingLoc[1] < 7:
            super().checkShortMove(board, possibleMoves, kingLoc[0], kingLoc[1] + 1)

        # left move
        if kingLoc[1] > 0:
            super().checkShortMove(board, possibleMoves, kingLoc[0], kingLoc[1] - 1)

        cas = self.castling(locations, board)
        if cas:
            possibleMoves.extend(cas)
        print(possibleMoves)
        return possibleMoves

    def isCheck(self, board, location):
        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}

        opponentMoves = opponentPossibleMoves(board, colors)
        # print(opponentMoves)
        # print(location)
        for a, b in opponentMoves:
            if (a, b) == location:
                # print('szach')
                return True
        return False

    def isCheckMate(self, board):

        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}

        for a in range(8):
            for b in range(8):
                if board[a][b] != ' ':
                    if board[a][b].color == colors['friendly']:
                        locations = {'figure': (a, b), 'field': False}
                        moves = board[a][b].possibleMoves(locations, board)
                        possibleMoves = isMoveCorrect(moves, locations['figure'], board)
                        if len(possibleMoves) > 0:
                            return False
        print(f'{self.color} sszach mat')
        return True

    @staticmethod
    def lookForKing(color, board):
        if color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}
        for a in range(8):
            for b in range(8):
                if isinstance(board[a][b], King):
                    if board[a][b].color == colors['friendly']:
                        return a, b

    def castling(self, locations, board):
        possibleMoves = []
        kingLoc = locations['figure']

        if not self.was_moving and not self.check:
            if board[kingLoc[0]][kingLoc[1]-1] == ' ' and board[kingLoc[0]][kingLoc[1]-2] == ' ' and board[kingLoc[0]][kingLoc[1]-3] == ' ':
                if type(board[kingLoc[0]][kingLoc[1]-4]) == Rook:
                    if board[kingLoc[0]][kingLoc[1]-4].color == self.color and not board[kingLoc[0]][kingLoc[1]-4].was_moving:
                        m = [(kingLoc[0], kingLoc[1]-1), (kingLoc[0], kingLoc[1]-2)]
                        moves = isMoveCorrect(m, (kingLoc[0], kingLoc[1]), board)
                        # print(moves)
                        if len(moves) == 2:

                            possibleMoves.append(moves[1])

            if board[kingLoc[0]][kingLoc[1]+1] == ' ' and board[kingLoc[0]][kingLoc[1]+2] == ' ':
                if type(board[kingLoc[0]][kingLoc[1]+3]) == Rook:
                    if board[kingLoc[0]][kingLoc[1]+3].color == self.color and not board[kingLoc[0]][kingLoc[1]+3].was_moving:
                        m = [(kingLoc[0], kingLoc[1]+1), (kingLoc[0], kingLoc[1]+2)]
                        moves = isMoveCorrect(m, (kingLoc[0], kingLoc[1]), board)
                        # print(moves)
                        if len(moves) == 2:
                            possibleMoves.append(moves[1])
        return possibleMoves



def isMoveCorrect(moves, figureLoc, board):
    movesToDel = []
    color = board[figureLoc[0]][figureLoc[1]].color

    for i, (a, b) in enumerate(moves):

        buf = board[a][b]
        if board[a][b] != ' ':
            board[a][b] = ' '

        (board[a][b], board[figureLoc[0]][figureLoc[1]]) = (board[figureLoc[0]][figureLoc[1]], board[a][b])
        kingLoc = King.lookForKing(color, board)
        if King.isCheck(board[kingLoc[0]][kingLoc[1]], board, kingLoc):
            movesToDel.append((a, b))
        (board[a][b], board[figureLoc[0]][figureLoc[1]]) = (board[figureLoc[0]][figureLoc[1]], board[a][b])
        board[a][b] = buf
    if len(movesToDel) > 0:
        for a in movesToDel:
            i = moves.index(a)
            del moves[i]
    return moves


def opponentPossibleMoves(board, colors):
    tab = [Queen, Knight, Pawn, Rook, Bishop]
    allMoves = []
    for a, line in enumerate(board):
        for b, value in enumerate(line):
            try:
                for c in tab:
                    if isinstance(board[a][b], c) and board[a][b].color == colors['opponent']:
                        locations = {'figure': (a, b), 'field': False}
                        moves = board[a][b].possibleMoves(locations, board)
                        allMoves += moves
                        break
            except:
                pass
    return allMoves


def castlingMove(board, figLoc, fieldLoc, rookPos):
    board[figLoc[0]][figLoc[1]].y = fieldLoc[0] * 90
    board[figLoc[0]][figLoc[1]].x = fieldLoc[1] * 90
    board[figLoc[0]][rookPos[0]].x = rookPos[1]*90
    (board[figLoc[0]][figLoc[1]], board[fieldLoc[0]][fieldLoc[1]]) = (board[fieldLoc[0]][fieldLoc[1]], board[figLoc[0]][figLoc[1]])
    (board[figLoc[0]][rookPos[0]], board[figLoc[0]][rookPos[1]]) = (board[figLoc[0]][rookPos[1]], board[figLoc[0]][rookPos[0]])