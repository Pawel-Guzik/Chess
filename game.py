from time import sleep


class Game():
    def __init__(self, id):
        self.id = id
        self.pTimes = [20, 20]
        self.players = ['white', 'black']
        self.was_moving = []
        self.move = ''
        self.turn = 'white'
        self.isPromotion = False
        self.promoFigure = ' '
        self.asked = []
        self.nicknames = []
        self.winner = ''
        self.areTwoPlayers = False

    def encodeTime(self):
        return str(self.pTimes[0]) + ' ' + str(self.pTimes[1])

    def timer(self, player):
        while self.pTimes[player] >= 0:
            if self.players[player] == self.turn:
                self.pTimes[player] -= 1
                sleep(1)

