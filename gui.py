import tkinter as tk
import mysql.connector
from dotenv import load_dotenv
import os
from datetime import datetime
load_dotenv('.env')

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd= os.getenv('passwd'),
    database='tescik'
)

class Gui(tk.Frame):

    def __init__(self, *args, **kwargs):
        self.root = self.rt()
        self.black = '#6B8E23'
        self.white = '#EFECA2'
        self.startGame = False
        self.loggedUser = ""
        self.userInfo = ""
        self.visible = True
        self.isRunning = True

        tk.Frame.__init__(self, self.root, bg=self.black, *args, **kwargs)
        self.nicknameLabel = tk.Label(self, text="NICKNAME", pady=10, bg=self.black, font='arial', fg=self.white)
        self.passwordLabel = tk.Label(self, text="PASSWORD", pady=4, bg=self.black, font='arial', fg=self.white)
        self.loginField = tk.Entry(self, width=25, font='arial', bg=self.white, fg=self.black)
        self.passwordField = tk.Entry(self, width=25, font='arial', show="*" , bg=self.white, fg=self.black)
        self.loginButton = tk.Button(self, text="LOG IN", command=self.login, pady=5, bg=self.white, font='arial')
        self.confirmLabel = tk.Label(self, text="CONFIRM PASSWORD", pady=4, bg=self.black, font='arial', fg=self.white)
        self.confirmPasswordField = tk.Entry(self, width=25, font='arial', show="*" , bg=self.white, fg=self.black)
        self.registerButton = tk.Button(self, text="REGISTER", command=self.register, pady=5, bg=self.white, font='arial')
        self.createButton = tk.Button(self, text="CREATE AN ACCOUNT", command=self.createAccount, pady=5, bg=self.white, font='arial')
        self.errorLabel = tk.Label(self, text="error[1]", pady=4, bg=self.black, font='arial', fg='red')
        self.goBackButton = tk.Button(self, text="GO BACK", command=self.loginView, pady=5, bg=self.white, font='arial')

        self.playButton = tk.Button(self, text="PLAY CHESS", command=self.play, pady=5, bg=self.white, font='arial')
        self.gameHistoryButton = tk.Button(self, text="GAME HISTORY", command=self.gameHistory, pady=5, bg=self.white, font='arial')
        self.rankingButton = tk.Button(self, text="RANKING", command=self.ranking, pady=5, bg=self.white, font='arial')

        self.quitButton = tk.Button(self, text="LOGOUT", command=self.quit, pady=5, bg=self.white, font='arial')
        self.menuButton = tk.Button(self, text="BACK", command=self.menu, pady=5, bg=self.white, font='arial')

        self.loginView()



    def quit(self):
        self.isRunning = False
    def resetGrid(self):
        for label in self.grid_slaves():
            label.grid_forget()

    def login(self):
        db.commit()
        mycursor = db.cursor()
        nick = self.loginField.get()
        passw = self.passwordField.get()
        mycursor.execute("SELECT nickname, password, points FROM user WHERE nickname = %s and password = %s", (nick, passw))
        check = mycursor.fetchone()
        if check is not None:
            self.loggedUser = check[0]
            self.userInfo = check[0] + ' ' + str(check[2])
            self.menu()




    def register(self):
        self.resetGrid()
        self.nicknameLabel.grid(row=0, column=0)
        self.loginField.grid(row=1, column=0)
        self.passwordLabel.grid(row=2, column=0)
        self.passwordField.grid(row=3, column=0)
        self.confirmLabel.grid(row=4, column=0)
        self.confirmPasswordField.grid(row=5, column=0)
        self.createButton.grid(row=6, column=0, pady=10)
        self.goBackButton.grid(row=7, column=0)

    def loginView(self):
        self.resetGrid()
        self.nicknameLabel.grid(row=0, column=0)
        self.loginField.grid(row=1, column=0)
        self.passwordLabel.grid(row=2, column=0)
        self.passwordField.grid(row=3, column=0)
        self.loginButton.grid(row=4, column=0, pady=10)
        self.registerButton.grid(row=5, column=0, pady=10)

    def createAccount(self):

        error = [False, '']
        mycursor = db.cursor()
        nick = self.loginField.get()
        password = self.passwordField.get()
        passwordConfirm = self.confirmPasswordField.get()

        if password == passwordConfirm and password != '' and nick != '':
            mycursor.execute("SELECT nickname FROM user WHERE nickname = %s", (nick,))
            check = mycursor.fetchone()
            if check is None:
                mycursor.execute("INSERT INTO user (nickname, password) VALUES (%s,%s)", (nick, password))
                db.commit()
                self.resetGrid()
                self.loginView()
                self.clearFields()
            else:
                error = [True, 'Nickname is already used']
                self.clearFields()
        else:
            self.clearFields()
            error = [True, 'Invalid Password!']

        if error[0] == True:
            self.errorLabel = tk.Label(self, text=error[1], pady=4, bg=self.white, font='arial', fg='red')
            self.errorLabel.grid(row=8, column=0)

    def clearFields(self):
        self.loginField.delete(0, 'end')
        self.passwordField.delete(0, 'end')
        self.confirmPasswordField.delete(0, 'end')

    def menu(self):
        self.resetGrid()
        tk.Label(self, text=self.userInfo, pady=4, bg=self.black, font=('arial',25), fg=self.white).grid(row=0, column=0)
        self.playButton.grid(row=1, column=0, pady=15)
        self.gameHistoryButton.grid(row=2, column=0, pady=15)
        self.rankingButton.grid(row=3, column=0, pady=15)
        self.quitButton.grid(row=4, column=0, pady=15)


    def play(self):
        self.startGame = True
        self.visible = False
        # self.playButton['state'] = tk.DISABLED
        self.root.withdraw()


    def gameHistory(self):
        db.commit()
        self.resetGrid()
        mycursor = db.cursor()
        mycursor.execute("SELECT * FROM game_history WHERE P1_nick=%s or P2_nick=%s", (self.loggedUser, self.loggedUser))
        allGames = mycursor.fetchall()
        tk.Label(self, text="GAME HISTORY", pady=4, bg=self.black, font=('arial', 25), fg=self.white).grid(row=0, column=0)
        for row_number, game in enumerate(allGames):
            if row_number == 10:
                break
            ltxt = f'{row_number+1}. {game[1]} vs {game[2]}'
            if game[3] == self.loggedUser:
                color = '#33ff00'
            else:
                color = 'red'
            tk.Label(self, text=ltxt, pady=4, bg=self.black, font=('arial', 15), fg=color).grid(row=row_number+1, column=0)
        self.menuButton.grid(row=12, column=0)
        print(datetime.now())

    def ranking(self):
        db.commit()
        self.resetGrid()
        mycursor = db.cursor()
        mycursor.execute("SELECT nickname, points FROM user ORDER BY points DESC")
        allUsers = mycursor.fetchall()
        tk.Label(self, text="TOP 10 PLAYERS", pady=4, bg=self.black, font=('arial', 25), fg=self.white).grid(row=0, column=0)
        for pos, player in enumerate(allUsers):
            if pos == 10:
                break
            txt = f'{(pos+1):2} {player[0]:8} {player[1]:5}'
            tk.Label(self, text=txt, pady=4, bg=self.black, font=('arial', 15), fg=self.white).grid(row=pos + 1, column=0)
        self.menuButton.grid(row=12, column=0)

    @staticmethod
    def rt():
        root = tk.Tk()
        root.title('Chess')
        root.configure(background='#6B8E23')
        positionRight = int(root.winfo_screenwidth() / 2 - 500 / 2)
        positionDown = int(root.winfo_screenheight() / 2 - 500 / 2)
        root.geometry("500x500+{}+{}".format(positionRight, positionDown))
        return root
