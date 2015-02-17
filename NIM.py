# Author: Yuki, Kapeeshan
# Date: 2012-01-10
# Purpose: to play the NIM game.
# Input: mouse click
# Output: a NIM game

from Tkinter import*
import random
import tkMessageBox

# Pile class
# Fields:
#   canvas: this is where the stones going to be drawed on
#   picture: random picture represent stone
#   y: the coordinate of this pile
#   value: the number of stone in the pile
# Methods:
#   constructor
#   draw: clear the area, then draw the stones.
#   remove: remove given number of stone, reduce the value.
#   removeFrom: removes all stones from the pile starting at given position
class Pile:

    # constructor
    # Parameter: canvas(where the pile going to be drawed on), y(the coordinate)
    def __init__ (self, canvas, y):
        self.canvas = canvas
        self.picture = PhotoImage(file = random.choice( ["a.gif", "b.gif", "c.gif"] ) )
        self.y = y
        self.value = random.randint(1, 30)

    # draw
    # Purpose: clear the area, then draw the stones.
    # Parameters: None
    # Return: none
    def draw(self):
        canvas.create_line(0, self.y, 800, self.y, width=40, fill="light cyan")
        x = 40
        for i in range(self.value): 
            canvas.create_image(x, self.y, anchor = NW, image = self.picture)
            canvas.update()
            x = x + 25
        canvas.create_text( 10, self.y, anchor = NW, text = str(self.value), \
                        font = ("Algerian", "15"))
        canvas.update()

    # remove
    # Purpose: remove given number of stone, reduce the value.
    # Parameters: x(the number of stone that need to be reduce)
    # Return: none
    def remove(self, x):
        self.value = self.value - x

    # removeFrom
    # Purpose: removes all stones from the pile starting at given position
    # Parameters: x(the position)
    # Return: none
    def removeFrom(self, x):
        self.value = x - 1
            
##############################################################################

# NIMGame class
# Fields:
#   piles: a list of 8 Pile objects
#   k: the number of piles a player can take from in a single turn
#   first: a variable indicating who goes first
#   userWent: a boolean to indicate if the user has taken a stone
#   userPiles: a list to keep track of which piles the user has taken from
#   win: pop out a message box if the user win
#   lose: pop out a message box if the user lose
# Methods:
#   constructor
#   gameOver: a boolean function indicating if the game is over
#   computersMove: show the computer's move in a single turn.
#   validUserMove: checks that if the user's move is valid
#   userMove: show the user's move in a single turn
class NIMGame:

    # constructor
    # Parameter:k (number of piles a player can take from in a single turn)
    #           first(a variable indicating who goes first)
    def __init__ (self, k, first):
        self.piles = []
        y = 20
        for i in range(8):
            self.piles.append( Pile(canvas, y) )
            y = y + 50
        self.k = k
        self.first = first
        self.userWent = False
        self.userPiles = []
        if self.first == 0:
            self.computersMove()

    # gameOver
    # Purpose: a boolean function indicating if the game is over
    # Parameters: none
    # Return: true or false
    def gameOver(self):
        x = 0
        for i in self.piles:
            if i.value != 0:
                x = x + 1
        return x == 0

    # computersMove
    # Purpose: show the computer's move in a single turn, also indicate who win
    # Parameters: None
    # Return: none
    def computersMove(self):
        if self.gameOver():
            self.lose()
        else:
            a = 0
            for n in range( len(self.piles) ):
                if self.piles[n].value > 0:
                    a = a + 1
                    m = n
            if a == 1 and self.piles[m].value == 1:
                self.piles[m].remove(1)
                self.piles[m].draw()
            elif a <= self.k and a >= 1:
                b = 0
                while self.piles[b].value == 0:
                    b = b + 1
                if self.piles[b].value > 1:
                    self.piles[b].remove(self.piles[b].value - 1)
                    self.piles[b].draw()
                b = b + 1
                if b < 8:
                    for l in range( b, 8):
                        self.piles[l].remove(self.piles[l].value)
                        self.piles[l].draw()
            else:
                x = random.randint(1,6)
                y = random.randint(0,x)
                z = random.randint(x,7)
                while self.piles[x].value == 0 and self.piles[y].value == 0  \
                    and self.piles[z].value == 0:
                    x = random.randint(0,7)
                    y = random.randint(0,x)
                    z = random.randint(x,7)
                if self.piles[x].value != 0:
                    self.piles[x].remove( random.randint( 1, self.piles[x].value ) )
                    self.piles[x].draw()
                if self.piles[y].value != 0:
                    self.piles[y].remove( random.randint( 1, self.piles[y].value ) )
                    self.piles[y].draw()
                if self.piles[z].value != 0:
                    self.piles[z].remove( random.randint( 1, self.piles[z].value ) )
                    self.piles[z].draw()      
            self.userWent = False
            self.userPiles = []
            if self.gameOver():
                self.win()

    # validUserMove
    # Purpose: checks that if the user's move is valid
    # Parameters: p(the pile that the player chose)
    #             s(the stone/position that the user click on)
    # Return: true or false
    def validUserMove(self, p, s):
        return p >= 0 and p <= 7    \
           and self.piles[p].value >= s and s > 0  \
           and ( p in self.userPiles or len(self.userPiles) < self.k )

    # userMove
    # Purpose: show the user's move in a single turn
    # Parameters: None
    # Return: none
    def userMove(self, p, s):
        if self.validUserMove(p, s):
            self.piles[p].removeFrom(s)
            self.piles[p].draw()
            self.userWent = True
            if p not in self.userPiles:
                self.userPiles.append(p)

    # win
    # Purpose: pop out a message box if the user win
    # Parameters: None
    # Return: none
    def win(self):
        picture = PhotoImage(file = "d.gif")
        canvas.create_image(400, 200, anchor = CENTER, image = picture)
        tkMessageBox.showinfo("Info", "~Congratulation!~ You win!~")

    # lose
    # Purpose: pop out a message box if the user lose
    # Parameters: None
    # Return: none
    def lose(self):
        picture = PhotoImage(file = "e.gif")
        canvas.create_image(400, 200, anchor = CENTER, image = picture)
        tkMessageBox.showinfo("Info", "~Sorry. You lose.~")


##############################################################################

# start
# Purpose: reset or start a new game
# Parameters: None
# Return: none
def start():
    canvas.create_rectangle(0, 0, 800, 400, outline = "", fill = "light cyan")
    global Nim
    k = kValue.get()
    first = firstGo.get()
    Nim = NIMGame(k, first)
    for i in range(8):
        Nim.piles[i].draw() 

# done
# Purpose: if the user went, let computer start to move
# Parameters: None
# Return: none    
def done():
    if Nim.userWent:
        Nim.computersMove()

# mouseClick
# Purpose: converts the mouse's y coordinate into a piles
#           and x coordinate into a stone location
# Parameters: event(mouse's coordinate)
# Return: none
def mouseClick(event):
    p = event.y / 50
    s = (event.x - 40) / 25 + 1
    Nim.userMove(p, s)

# about
# Purpose: pop out a window showing infomation about this game
# Parameters: None
# Return: none
def about():
    win=Tk()
    win.title("Grade 11 Computer Science")
    aboutlabel=Label(win, text = "Create by Kapeeshan and Yuki \
                     \n NIM is an ancient game in which players \
                     \n alternate taking stonesfrom various piles.\
                     \n The player who takes the last stone loses.",    \
                     width=40, font=("Bradley Hand ITC", "10"))
    aboutlabel.grid(row=0, column=0, sticky=W)

#############################################################################

root = Tk()
root.title("NIM game")
root.config(bg = "MediumPurple1")
canvas = Canvas(root, width = 800, height = 400)
canvas.config(background = "light cyan")
canvas.grid(row = 1, column = 0, columnspan = 3)
canvas.focus_set()
canvas.bind("<Button-1>",mouseClick)
picture = PhotoImage(file = "f.gif")
canvas.create_image(400, 200, anchor = CENTER, image = picture)

###################################### k #####################################

kValue = IntVar()
kValue.set(3)
a = Label(root, text = "k", \
           font = ("Algerian", "30"), bg = "MediumPurple1")
a.place(x = 30, y = 25)
w = OptionMenu(root, kValue, 1, 2, 3, 4, 5, 6, 7)
w.config(bg = "skyblue")  
w.grid(row = 0, column = 0, padx = 5, pady = 5)

########################### Who goes first buttons ############################

firstGo = IntVar()
firstGo.set( 0 )
firstgroup = LabelFrame(root, text = "Who goes first?",     \
                        font = ("Curlz MT",12),     \
                       padx = 4, pady = 4, bg = "DarkGoldenrod1") 
firstgroup.grid(row = 0, column = 1, padx = 5, pady = 5)

Radiobutton (firstgroup, text ="Computer", font = ("Bradley Hand ITC",10),  \
             variable = firstGo, value = 0, bg = "DarkGoldenrod1")   \
             .grid(row = 0, sticky = W) 

Radiobutton (firstgroup, text = "Human", font = ("Bradley Hand ITC",10),    \
             variable = firstGo, value = 1, bg = "DarkGoldenrod1")    \
             .grid(row = 1, sticky = W)

################################# Menu ########################################

menubar=Menu(root)
filemenu = Menu(menubar, tearoff = 0)
filemenu.add_command(label = "Start new game", command = lambda:start())
filemenu.add_command(label = "Exit",
                     command = lambda:root.destroy())
menubar.add_cascade(label = "Menu", menu = filemenu)

################################## k menu ###################################

kmenu=Menu(menubar, tearoff = 0)
kmenu.add_checkbutton(label = "1", variable = kValue, onvalue = 1)
kmenu.add_checkbutton(label = "2", variable = kValue, onvalue = 2)
kmenu.add_checkbutton(label = "3", variable = kValue, onvalue = 3)
kmenu.add_checkbutton(label = "4", variable = kValue, onvalue = 4)
kmenu.add_checkbutton(label = "5", variable = kValue, onvalue = 5)
kmenu.add_checkbutton(label = "6", variable = kValue, onvalue = 6)
kmenu.add_checkbutton(label = "7", variable = kValue, onvalue = 7)
menubar.add_cascade(label="k value", menu=kmenu)

################################## first menu ###################################

firstmenu=Menu(menubar, tearoff = 0)
firstmenu.add_checkbutton(label = "Computer", variable = firstGo, onvalue = 0)
firstmenu.add_checkbutton(label = "Human", variable = firstGo, onvalue = 1)
menubar.add_cascade(label="who goes first", menu=firstmenu)

################################ Help Menu ###################################

helpmenu=Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=lambda:about())
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu = menubar)


################################## Start button ###############################

buttonStart = Button (root, text = "Start", font = ("Curlz MT",15,"bold"),   \
                      width = 10, height = 1, bg = "tomato",  \
                      command = lambda:start())

buttonStart.grid(row = 0, column = 2, sticky = W,   \
                 padx = 10, pady = 5)

################################## Done button ###############################

buttonDone = Button(root, text = "Done", font = ("Curlz MT",15,"bold"),    \
                    width = 10, height = 1, bg = "spring green",    \
                    command = lambda:done())

buttonDone.grid(row = 0, column = 2, sticky = E,    \
                padx = 10, pady = 5)


mainloop()
