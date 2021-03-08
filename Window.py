import pygame


class Window:
    colors = [['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
              ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
              ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
              ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
              ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
              ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w'],
              ['w', 'b', 'w', 'b', 'w', 'b', 'w', 'b'],
              ['b', 'w', 'b', 'w', 'b', 'w', 'b', 'w']]

    def __init__(self):
        self.surface = pygame.display.set_mode((720, 720))
        self.black = (107, 142, 35)
        self.white = (239, 236, 162)
        self.highlightColor = (70, 105, 73)
        self.prevmoveColor = {'black': (149, 142, 40), 'white': (174, 167, 75)}



    def highlightPreviousMove(self, locations, moveLoc):

        squareSize = 90
        figLoc = locations['figure']

        if figLoc is not False:
            if self.colors[figLoc[0]][figLoc[1]] == 'w':
                pygame.draw.rect(self.surface, self.prevmoveColor['white'],
                                 (figLoc[1] * squareSize, figLoc[0] * squareSize, squareSize, squareSize))
            elif self.colors[figLoc[0]][figLoc[1]] == 'b':
                pygame.draw.rect(self.surface, self.prevmoveColor['black'],
                                 (figLoc[1] * squareSize, figLoc[0] * squareSize, squareSize, squareSize))

        if not len(moveLoc) == 0:
            if self.colors[moveLoc[0][1]][moveLoc[0][0]] == 'w':
                pygame.draw.rect(self.surface, self.prevmoveColor['white'],
                                 (moveLoc[0][1] * squareSize, moveLoc[0][0] * squareSize, squareSize, squareSize))
            else:
                pygame.draw.rect(self.surface, self.prevmoveColor['black'],
                                 (moveLoc[0][1] * squareSize, moveLoc[0][0] * squareSize, squareSize, squareSize))
            if self.colors[moveLoc[1][1]][moveLoc[1][0]] == 'w':

                pygame.draw.rect(self.surface, self.prevmoveColor['white'],
                                 (moveLoc[1][1] * squareSize, moveLoc[1][0] * squareSize, squareSize, squareSize))
            else:
                pygame.draw.rect(self.surface, self.prevmoveColor['black'],
                                 (moveLoc[1][1] * squareSize, moveLoc[1][0] * squareSize, squareSize, squareSize))




    def highlightPossibleMoves(self, moves, board, moveLoc):
        for x, y in moves:
            if board[x][y] != ' ':

                pygame.draw.circle(self.surface, self.highlightColor, (y * 90 + 45, x * 90 + 45), 45)

                if self.colors[x][y] == 'w':
                    if (x, y) == moveLoc[1]:
                        pygame.draw.circle(self.surface, self.prevmoveColor['white'], (y * 90 + 45, x * 90 + 45), 40)
                    else:
                        pygame.draw.circle(self.surface, self.white, (y * 90 + 45, x * 90 + 45), 40)
                elif self.colors[x][y] == 'b':
                    if (x, y) == moveLoc[1]:
                        pygame.draw.circle(self.surface, self.prevmoveColor['black'], (y * 90 + 45, x * 90 + 45), 40)
                    else:
                        pygame.draw.circle(self.surface, self.black, (y * 90 + 45, x * 90 + 45), 40)




            else:
                pygame.draw.circle(self.surface, self.highlightColor, (y * 90 + 45, x * 90 + 45), 15)


    def drawBoard(self, moves, board, locations, moveLoc):
        squareSize = 90
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(self.surface, self.white,
                                     (i * squareSize, j * squareSize, squareSize, squareSize))
                else:
                    pygame.draw.rect(self.surface, self.black,
                                     (i * squareSize, j * squareSize, squareSize, squareSize))



        self.highlightPreviousMove(locations, moveLoc)


        self.highlightPossibleMoves(moves, board, moveLoc)


        for a, line in enumerate(board):
            for b, column in enumerate(line):
                if board[a][b] != ' ':
                    self.surface.blit(board[a][b].img, (board[a][b].x, board[a][b].y))
