import pygame


class Pawn:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.is_possible = True
        self.was_moving = False
        if color == 'black':
            self.img = pygame.image.load('img/C_Pion.png')
        if color == 'white':
            self.img = pygame.image.load('img/B_Pion.png')

    def __str__(self):
        return f'{self.color} Pawn ({self.x},{self.y})'

    def isMovePossible(self, locations, board):
        pawnLoc = locations['figure']


        possibleMoves = []

        if self.color == 'white':

            if pawnLoc[0] > 0:
                # ruch do przodu
                if board[pawnLoc[0] - 1][pawnLoc[1]] == ' ':

                    possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1]))

                # zbicie w prawo
                if pawnLoc[1] < 7:
                    if board[pawnLoc[0] - 1][pawnLoc[1] + 1] != ' ':
                        if board[pawnLoc[0] - 1][pawnLoc[1] + 1].color == 'black':

                            possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1] + 1))

                # zbicie w lewo
                if pawnLoc[1] > 0:
                    if board[pawnLoc[0] - 1][pawnLoc[1] - 1] != ' ':
                        if board[pawnLoc[0] - 1][pawnLoc[1] - 1].color == 'black':

                            possibleMoves.append((pawnLoc[0] - 1, pawnLoc[1] - 1))


            #ruch o dwa do przodu
                if self.was_moving is False and board[pawnLoc[0] - 1][pawnLoc[1]] == ' ' and board[pawnLoc[0] - 2][pawnLoc[1]] == ' ':
                    possibleMoves.append((pawnLoc[0] - 2, pawnLoc[1]))


        if self.color == 'black':
            # ruch do przodu
            if pawnLoc[0] < 7:
                if board[pawnLoc[0] + 1][pawnLoc[1]] == ' ':
                    possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1]))

            # zbicie w prawo
                if pawnLoc[1] < 7:
                    if board[pawnLoc[0] + 1][pawnLoc[1] + 1] != ' ':
                        if board[pawnLoc[0] + 1][pawnLoc[1] + 1].color == 'white':
                            possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1] + 1))

            # zbicie w lewo
                if pawnLoc[1] > 0:
                    if board[pawnLoc[0] + 1][pawnLoc[1] - 1] != ' ':
                        if board[pawnLoc[0] + 1][pawnLoc[1] - 1].color == 'white':
                            possibleMoves.append((pawnLoc[0] + 1, pawnLoc[1] - 1))

            if self.was_moving is False and board[pawnLoc[0] + 1][pawnLoc[1]] == ' ' and board[pawnLoc[0] + 2][pawnLoc[1]] == ' ':
                possibleMoves.append((pawnLoc[0] + 2, pawnLoc[1]))



        return possibleMoves




class Knight:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.is_possible = True
        if color == 'black':
            self.img = pygame.image.load('img/C_Kon.png')
        if color == 'white':
            self.img = pygame.image.load('img/B_Kon.png')


    def isMovePossible(self, locations, board):
        knightLoc = locations['figure']
        possibleMoves = []
        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}
        print(knightLoc)
        print('esten')

        # ruchy w lewo dół

        if knightLoc[0] < 7 and knightLoc[1] > 1:
            if board[knightLoc[0]+1][knightLoc[1]-2] == ' ':
                possibleMoves.append((knightLoc[0] + 1, knightLoc[1] - 2))
            else:
                if board[knightLoc[0]+1][knightLoc[1]-2].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0]+1, knightLoc[1]-2))

        if knightLoc[0] < 6 and knightLoc[1] > 0:
            if board[knightLoc[0]+2][knightLoc[1]-1] == ' ':
                possibleMoves.append((knightLoc[0] + 2, knightLoc[1] - 1))
            else:
                if board[knightLoc[0]+2][knightLoc[1]-1].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0]+2, knightLoc[1]-1))

        # ruchy w prawo dół

        if knightLoc[0] < 7 and knightLoc[1] < 6:
            if board[knightLoc[0] + 1][knightLoc[1] + 2] == ' ':
                possibleMoves.append((knightLoc[0] + 1, knightLoc[1] + 2))
            else:
                if board[knightLoc[0] + 1][knightLoc[1] + 2].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0] + 1, knightLoc[1] + 2))

        if knightLoc[0] < 6 and knightLoc[1] < 7:
            if board[knightLoc[0] + 2][knightLoc[1] + 1] == ' ':
                possibleMoves.append((knightLoc[0] + 2, knightLoc[1] + 1))
            else:
                if board[knightLoc[0] + 2][knightLoc[1] + 1].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0] + 2, knightLoc[1] + 1))

        # ruchy w prawo góra

        if knightLoc[0] > 0 and knightLoc[1] < 6:
            if board[knightLoc[0] - 1][knightLoc[1] + 2] == ' ':
                possibleMoves.append((knightLoc[0] - 1, knightLoc[1] + 2))
            else:
                if board[knightLoc[0] -1][knightLoc[1] + 2].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0] - 1, knightLoc[1] + 2))

        if knightLoc[0] > 1 and knightLoc[1] < 7:
            if board[knightLoc[0] - 2][knightLoc[1] + 1] == ' ':
                possibleMoves.append((knightLoc[0] - 2, knightLoc[1] + 1))
            else:
                if board[knightLoc[0] - 2][knightLoc[1] + 1].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0] - 2, knightLoc[1] + 1))



        # ruchy w lewo góra

        if knightLoc[0] > 0 and knightLoc[1] > 1:
            if board[knightLoc[0] - 1][knightLoc[1] - 2] == ' ':
                possibleMoves.append((knightLoc[0] - 1, knightLoc[1] - 2))
            else:
                if board[knightLoc[0] - 1][knightLoc[1] - 2].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0] - 1, knightLoc[1] - 2))

        if knightLoc[0] > 1 and knightLoc[1] > 0:
            if board[knightLoc[0] - 2][knightLoc[1] - 1] == ' ':
                possibleMoves.append((knightLoc[0] - 2, knightLoc[1] - 1))
            else:
                if board[knightLoc[0] - 2][knightLoc[1] - 1].color == colors['opponent']:
                    possibleMoves.append((knightLoc[0] - 2, knightLoc[1] - 1))



        print(possibleMoves)

        return possibleMoves





class Bishop:

    # polozenie piona (wiersz, kolumna)

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.is_possible = False
        if color == 'black':
            self.img = pygame.image.load('img/C_Goniec.png')
        if color == 'white':
            self.img = pygame.image.load('img/B_Goniec.png')

    def isMovePossible(self, locations, board):
        bishopLoc = locations['figure']
        possibleMoves = []
        # ruch w lewy dół
        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}
        print(bishopLoc)

        if bishopLoc[0] < 7 and bishopLoc[1] > 0:
            print('lewodol')

            for i in range(1,8):
                if bishopLoc[0] + i > 7 or bishopLoc[1] - i < 0:
                    break

                if board[bishopLoc[0] + i][bishopLoc[1] - i] != ' ':
                    if board[bishopLoc[0] + i][bishopLoc[1] - i].color == colors['friendly']:
                        break
                    elif board[bishopLoc[0] + i][bishopLoc[1] - i].color == colors['opponent']:
                        possibleMoves.append((bishopLoc[0] + i, bishopLoc[1] - i))
                        break
                else:
                    possibleMoves.append((bishopLoc[0] + i, bishopLoc[1] - i))

        # ruch lewo gora

        if bishopLoc[0] > 0 and bishopLoc[1] > 0:

            for i in range(1, 8):
                print('lewogora')
                if bishopLoc[0] - i < 0 or bishopLoc[1] - i < 0:
                    break

                if board[bishopLoc[0] - i][bishopLoc[1] - i] != ' ':
                    if board[bishopLoc[0] - i][bishopLoc[1] - i].color == colors['friendly']:
                        break
                    elif board[bishopLoc[0] - i][bishopLoc[1] - i].color == colors['opponent']:
                        possibleMoves.append((bishopLoc[0] - i, bishopLoc[1] - i))
                        break
                else:

                    possibleMoves.append((bishopLoc[0] - i, bishopLoc[1] - i))

        #ruch w prawo dol

        if bishopLoc[0] < 7 and bishopLoc[1] < 7:
            print('prawodol')
            for i in range(1, 8):
                if bishopLoc[0] + i > 7 or bishopLoc[1] + i > 7:
                    break

                if board[bishopLoc[0] + i][bishopLoc[1] + i] != ' ':
                    if board[bishopLoc[0] + i][bishopLoc[1] + i].color == colors['friendly']:
                        break
                    elif board[bishopLoc[0] + i][bishopLoc[1] + i].color == colors['opponent']:
                        possibleMoves.append((bishopLoc[0] + i, bishopLoc[1] + i))
                        break
                else:
                    possibleMoves.append((bishopLoc[0] + i, bishopLoc[1] + i))

        #ruch w prawo gora
        if bishopLoc[0] > 0 and bishopLoc[1] < 7:


            for i in range(1, 8):
                if bishopLoc[0] - i < 0 or bishopLoc[1] + i > 7:
                    break

                if board[bishopLoc[0] - i][bishopLoc[1] + i] != ' ':
                    if board[bishopLoc[0] - i][bishopLoc[1] + i].color == colors['friendly']:
                        break
                    elif board[bishopLoc[0] - i][bishopLoc[1] + i].color == colors['opponent']:

                        possibleMoves.append((bishopLoc[0] - i, bishopLoc[1] + i))
                        break
                else:
                    possibleMoves.append((bishopLoc[0] - i, bishopLoc[1] + i))


        print(possibleMoves)

        return possibleMoves







class Rook:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.is_possible = False
        if color == 'black':
            self.img = pygame.image.load('img/C_Wieza.png')
        if color == 'white':
            self.img = pygame.image.load('img/B_Wieza.png')

    def isMovePossible(self, locations, board):
        rookLoc = locations['figure']
        possibleMoves = []
        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}
        print(rookLoc)

        #ruchy w dół

        if rookLoc[0] < 7:
            for a in range(1,8):
                if rookLoc[0]+a == 8:
                    break
                else:
                    if board[rookLoc[0]+a][rookLoc[1]] == ' ':
                        possibleMoves.append((rookLoc[0]+a, rookLoc[1]))
                    else:
                        if board[rookLoc[0]+a][rookLoc[1]].color == colors['friendly']:
                            break
                        if board[rookLoc[0]+a][rookLoc[1]].color == colors['opponent']:
                            possibleMoves.append((rookLoc[0]+a, rookLoc[1]))
                            break
        # ruchy w góre

        if rookLoc[0] > 0:
            for a in range(1,8):
                if rookLoc[0] - a == -1:
                    break
                else:
                    if board[rookLoc[0]-a][rookLoc[1]] == ' ':
                        possibleMoves.append((rookLoc[0]-a, rookLoc[1]))
                    else:
                        if board[rookLoc[0]-a][rookLoc[1]].color == colors['friendly']:
                            break
                        if board[rookLoc[0]-a][rookLoc[1]].color == colors['opponent']:
                            possibleMoves.append((rookLoc[0]-a, rookLoc[1]))
                            break
        # ruchy w prawo

        if rookLoc[1] < 7:
            for a in range(1,8):
                if rookLoc[1]+a == 8:
                    break
                else:
                    if board[rookLoc[0]][rookLoc[1]+a] == ' ':
                        possibleMoves.append((rookLoc[0], rookLoc[1]+a))
                    else:
                        if board[rookLoc[0]][rookLoc[1]+a].color == colors['friendly']:
                            break
                        if board[rookLoc[0]][rookLoc[1]+a].color == colors['opponent']:
                            possibleMoves.append((rookLoc[0], rookLoc[1]+a))
                            break
        # ruchy w lewo
        if rookLoc[1] > 0:
            for a in range(1,8):
                if rookLoc[1] - a == -1:
                    break
                else:
                    if board[rookLoc[0]][rookLoc[1]-a] == ' ':
                        possibleMoves.append((rookLoc[0], rookLoc[1]-a))
                    else:
                        if board[rookLoc[0]][rookLoc[1]-a].color == colors['friendly']:
                            break
                        if board[rookLoc[0]][rookLoc[1]-a].color == colors['opponent']:
                            possibleMoves.append((rookLoc[0], rookLoc[1]-a))
                            break

        return possibleMoves



class Queen:

    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.is_possible = False
        if color == 'black':
            self.img = pygame.image.load('img/C_Dama.png')
        if color == 'white':
            self.img = pygame.image.load('img/B_Dama.png')

    def isMovePossible(self, locations, board):
        a = Rook.isMovePossible(self, locations, board)
        b = Bishop.isMovePossible(self, locations, board)
        possibleMoves = a+b
        return possibleMoves


class King:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.is_possible = False
        self.check = False
        if color == 'black':
            self.img = pygame.image.load('img/C_Krol.png')
        if color == 'white':
            self.img = pygame.image.load('img/B_Krol.png')

    def isMovePossible(self, locations, board):
        possibleMoves = []
        kingLoc = locations['figure']
        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}




        if kingLoc[0] > 0:

            # ruch w góre
            if board[kingLoc[0]-1][kingLoc[1]] == ' ':
                possibleMoves.append((kingLoc[0]-1, kingLoc[1]))
            else:
                if board[kingLoc[0]-1][kingLoc[1]].color == colors['opponent']:
                    possibleMoves.append((kingLoc[0]-1, kingLoc[1]))
            # lewy górny róg
            if kingLoc[1] > 0:
                if board[kingLoc[0] - 1][kingLoc[1]-1] == ' ':
                    possibleMoves.append((kingLoc[0] - 1, kingLoc[1]-1))
                else:
                    if board[kingLoc[0] - 1][kingLoc[1]-1].color == colors['opponent']:
                        possibleMoves.append((kingLoc[0] - 1, kingLoc[1]-1))

            # prawy górny róg
            if kingLoc[1] < 7:
                if kingLoc[1] > 0:
                    if board[kingLoc[0] - 1][kingLoc[1] + 1] == ' ':
                        possibleMoves.append((kingLoc[0] - 1, kingLoc[1] + 1))
                    else:
                        if board[kingLoc[0] - 1][kingLoc[1] + 1].color == colors['opponent']:
                            possibleMoves.append((kingLoc[0] - 1, kingLoc[1] + 1))


        #ruch w dól

        if kingLoc[0] < 7:
            if board[kingLoc[0]+1][kingLoc[1]] == ' ':
                possibleMoves.append((kingLoc[0]+1, kingLoc[1]))
            else:
                if board[kingLoc[0]+1][kingLoc[1]].color == colors['opponent']:
                    possibleMoves.append((kingLoc[0]+1, kingLoc[1]))
            # prawy dolny róg
            if kingLoc[1] < 7:
                if kingLoc[1] > 0:
                    if board[kingLoc[0] + 1][kingLoc[1] + 1] == ' ':
                        possibleMoves.append((kingLoc[0] + 1, kingLoc[1] + 1))
                    else:
                        if board[kingLoc[0] + 1][kingLoc[1] + 1].color == colors['opponent']:
                            possibleMoves.append((kingLoc[0] + 1, kingLoc[1] + 1))
            #lewy dolny rog
            if kingLoc[1] > 0:
                if board[kingLoc[0] + 1][kingLoc[1]-1] == ' ':
                    possibleMoves.append((kingLoc[0] + 1, kingLoc[1]-1))
                else:
                    if board[kingLoc[0] + 1][kingLoc[1]-1].color == colors['opponent']:
                        possibleMoves.append((kingLoc[0] + 1, kingLoc[1]-1))

        # ruch w prawo

        if kingLoc[1] < 7:
            if board[kingLoc[0]][kingLoc[1]+1] == ' ':
                possibleMoves.append((kingLoc[0], kingLoc[1]+1))
            else:
                if board[kingLoc[0]][kingLoc[1]+1].color == colors['opponent']:
                    possibleMoves.append((kingLoc[0], kingLoc[1]+1))
        # ruch w lewo

        if kingLoc[1] > 0:
            if board[kingLoc[0]][kingLoc[1]-1] == ' ':
                possibleMoves.append((kingLoc[0], kingLoc[1]-1))
            else:
                if board[kingLoc[0]][kingLoc[1]-1].color == colors['opponent']:
                    possibleMoves.append((kingLoc[0], kingLoc[1]-1))



        return possibleMoves



    def isCheck(self, board, location):


        # pion goniec kon krol dama wieza
        if self.color == 'black':
            colors = {'friendly': 'black', 'opponent': 'white'}
        else:
            colors = {'friendly': 'white', 'opponent': 'black'}

        # gora
        a = 1
        while location[0] - a != -1:
            if board[location[0]-a][location[1]] != ' ':
                if board[location[0]-a][location[1]].color == colors['friendly']:
                    break
                else:
                    if isinstance(board[location[0]-a][location[1]], Rook) or isinstance(board[location[0]-a][location[1]], Queen):
                        return True
            a+=1






        # dol
        a = 1
        while location[0] + a != 8:
            if board[location[0]+a][location[1]] != ' ':
                if board[location[0]+a][location[1]].color == colors['friendly']:
                    break
                else:
                    if isinstance(board[location[0]+a][location[1]], Rook) or isinstance(board[location[0]+a][location[1]], Queen):
                        return True
            a += 1


        # lewy skos góra
        a = 1
        while location[0] - a != -1 and location[1] - a != -1:
            if board[location[0] - a][location[1] - a] != ' ':
                if board[location[0] - a][location[1] - a].color == colors['opponent'] and isinstance(board[location[0] - a][location[1] - a], Pawn) and a == 1:
                    return True

                if board[location[0] - a][location[1] - a].color == colors['friendly']:
                    break
                else:
                    if isinstance(board[location[0] - a][location[1] - a], Bishop) or isinstance(board[location[0] - a][location[1] - a], Queen):
                        return True
            a += 1
        #prawy skos dół
        a = 1
        while location[0] + a != 8 and location[1] + a != 8:
            print(a)
            if board[location[0] + a][location[1] + a] != ' ':
                if board[location[0] + a][location[1] + a].color == colors['opponent'] and isinstance(board[location[0] + a][location[1] + a], Pawn) and a == 1:
                    return True

                if board[location[0] + a][location[1] + a].color == colors['friendly']:
                    break
                else:
                    if isinstance(board[location[0] + a][location[1] + a], Bishop) or isinstance(board[location[0] + a][location[1] + a], Queen):
                        return True
            a += 1

        #lewy skos dół
        a = 1
        while location[0] + a != 8 and location[1] - a != -1:
            if board[location[0] + a][location[1] - a] != ' ':
                if board[location[0] + a][location[1] - a].color == colors['opponent'] and isinstance(board[location[0] + a][location[1] - a], Pawn) and a == 1:
                    return True

                if board[location[0] + a][location[1] - a].color == colors['friendly']:
                    break
                else:
                    if isinstance(board[location[0] + a][location[1] - a], Bishop) or isinstance(board[location[0] + a][location[1] - a], Queen):
                        return True
            a += 1

        # prawy skos gora
        a = 1
        while location[0] - a != -1 and location[1] + a != 8:
            if board[location[0] - a][location[1] + a] != ' ':
                if board[location[0] - a][location[1] + a].color == colors['opponent'] and isinstance(board[location[0] - a][location[1] + a], Pawn) and a == 1:
                    return True

                if board[location[0] - a][location[1] + a].color == colors['friendly']:
                    break
                else:
                    if isinstance(board[location[0] - a][location[1] + a], Bishop) or isinstance(board[location[0] - a][location[1] + a], Queen):
                        return True
            a += 1







        return False


















