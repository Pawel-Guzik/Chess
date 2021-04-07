import pygame

pygame.font.init()

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
        self.width = 900
        self.height = 720
        self.surface = pygame.display.set_mode((self.width, self.height))
        self.black = (107, 142, 35)
        self.white = (239, 236, 162)
        self.highlightColor = (70, 105, 73)
        self.prevmoveColor = {'black': (149, 142, 40), 'white': (174, 167, 75)}
        self.font = pygame.font.SysFont('arial', 30)


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


    @staticmethod
    def formatTime(tup):
        minutes = str(tup[0])
        seconds = str(tup[1])
        if tup[1] > 9:
            return minutes + ':' + seconds
        else:
            return minutes + ":0" + seconds


    def drawInfo(self,times, nicknames):
        diplayTime = []
        nicknames = nicknames.split()
        pygame.draw.rect(self.surface, (6, 26, 0), (720, 0, 180, 720))
        player1Text = self.font.render(f' {nicknames[1]}', True, self.black)
        player2Text = self.font.render(f' {nicknames[0]}', True, self.black)
        for a in times:
            a = Window.formatTime(divmod(a, 60))
            diplayTime.append(a)
        p1Time = self.font.render(f'     {diplayTime[1]}', True, self.black)
        p2Time = self.font.render(f'     {diplayTime[0]}', True, self.black)
        self.surface.blit(player1Text, (720, 0))
        self.surface.blit(player2Text, (720, 680))
        self.surface.blit(p1Time, (720, 50))
        self.surface.blit(p2Time, (720, 630))



    def drawBoard(self, moves, board, locations, moveLoc, times, nicknames ,move = None, promotion = False,):
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
                    self.surface.blit(board[a][b].img, board[a][b].imgLoc)

        self.drawInfo(times, nicknames)
        if promotion:
            self.drawPromotionFigures(move)
        pygame.display.update()


    def menuScreen(self):
        self.surface.fill(self.black)
        pygame.draw.rect(self.surface, self.white, (300, 285, 300, 150))
        play = self.font.render('PLAY CHESS', True, self.black)
        self.surface.blit(play, (360, 345))
        pygame.display.update()

    def waitingForPlayer(self):
        self.surface.fill(self.black)
        com = self.font.render('WAITING FOR OTHER PLAYER...', True, self.white)
        self.surface.blit(com, (230, 345))
        pygame.display.update()

    def drawPromotionFigures(self, move):
        if move == 'white':
            col = 'B'
        elif move == 'black':
            col = 'C'
        bishop = pygame.image.load(f'img/{col}_Goniec.png')
        rook = pygame.image.load(f'img/{col}_Wieza.png')
        queen = pygame.image.load(f'img/{col}_Dama.png')
        knight = pygame.image.load(f'img/{col}_Kon.png')
        pygame.draw.rect(self.surface, (0, 128, 0), (720, 270, 180, 180))
        self.surface.blit(queen, (720, 270))
        self.surface.blit(rook, (810, 270))
        self.surface.blit(knight, (720, 360))
        self.surface.blit(bishop, (810, 360))

        pygame.display.update()



