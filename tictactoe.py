import RPi.GPIO as GPIO
import time, math
from os import system
import re

GPIO.setmode(GPIO.BOARD)

GPIO.setup(11, GPIO.IN)#down

GPIO.setup(13, GPIO.IN)#left

GPIO.setup(15, GPIO.IN)#up

GPIO.setup(16, GPIO.IN)#ok

GPIO.setup(18, GPIO.IN)#right

def clear():
    _ = system('clear')

class Player:
    name = ""
    def __init__(self, inName):
        self.name = inName
    
class Square:
    
    symbol = ' '
    isSet = False
    flag = 0
    
    def setLock(self):
        if (self.flag == 0):
            self.isSet = True
            self.flag = 1
        return
    def setSymbol(self, player):
        self.symbol = player.name

class Board:
   
    
    board = []
    #size = 1
    def __init__(self, inSize):
        self.size = inSize
        self.x_regex = re.compile(r'XXX')
        self.o_regex = re.compile(r'OOO')
    #CREATE LIST
    def createBoard(self):
        for i in range(self.size * self.size):
            self.board.append(makeSquare())
    
    #SETS THE PLAYER SYMBOLS IN THE BOARD
    def setBoard(self, player, pointer):
        #currentPosition = self.board[pointer.position]
        if(self.board[pointer.position].isSet == False):
                self.board[pointer.position].setLock()
                self.board[pointer.position].symbol = player.name
                
    
    #PRINTS THE WHOLE LIST
    def printBoard(self, player, pointer):
        clear()
        counter = 0

        print('Player: ', player.name)
        for square in self.board:
            #NEW LINE
            if(counter % self.size == 0):
                print()
                #PRINTS HORISONTAL LINES
                if(counter != 0):
                    for i in range (self.size):
                        print(" ---", end=' ')
                print()
            #PRINTS THE OBJECT
            if(counter == pointer.position and square.isSet == False):
                print('|', '#', end= ' |')
            else: 
                print('|', square.symbol, end= ' |')
            
                
            counter += 1
            
        print()
        
    def winnerControl(self, player):
        row = ''
        
        #LOOKS FOR THREE IN A ROW HORISONTAL
        counter = 0
        endCounter = self.size
        for j in range(0, self.size):
            for i in range(counter,endCounter):
                row += self.board[i].symbol
                if(self.x_regex.search(row)):
                    print('Player ', player.name, ' is the winner')
                    return
                if(self.o_regex.search(row)):
                    print('Player ', player.name, ' is the winner')
                    return
                    
            counter += self.size
            endCounter += self.size
            row = ''
            
        #LOOKS FOR THREE IN A ROW VERTICAL
        counter = 0
        for j in range(0, self.size):
            for i in range(counter,self.size*self.size-self.size+1, self.size):
                row += self.board[i].symbol
                if(self.x_regex.search(row)):
                    print('Player ', player.name, ' is the winner')
                    return
                if(self.o_regex.search(row)):
                    print('Player ', player.name, ' is the winner')
                    return     
            counter += 1
            row = ''
            
        #LOOKS FOR THREE IN A ROW SICK SACK
        counter = 0
        for i in range(0, self.size):
            row += self.board[i].symbol
            for j in range(counter, self.size*self.size):
                if((counter+self.size+1) < self.size ** 2):
                    row += self.board[(counter+self.size+1)].symbol
                if(self.x_regex.search(row)):
                    print('Player ', player.name, ' is the winner')
                    return
                if(self.o_regex.search(row)):
                    print('Player ', player.name, ' is the winner')
                    return
                counter += self.size + 1
            row = ''
            
        
            
class Pointer:
    position = 0
    size = 0
    okPressed = False
    def __init__(self, inSize):
        self.size = inSize
    def setPosition(self, button,player,board):
        okPressed = False
        if(button == 11): #down
            if(self.position <= ((self.size * self.size) -1) - self.size):
                self.position += self.size
        elif(button == 13): #left
            if(self.position != 0):
                self.position -= 1
        elif(button == 15): #up
            if(self.position >= self.size):
                self.position -= self.size
        elif(button == 18):#right
            if(self.position < (self.size * self.size) -1):
                self.position += 1
        elif(button == 16): #ok
            okPressed = True
            board.setBoard(player,pointer)



def makePlayer(name):
    x = Player(name)
    return x
def makeSquare():
    s = Square()
    return s
def makeBoard(size):
    board = Board(size)
    return board
def makePointer(size):
    pointer = Pointer(size)
    return pointer

#SETUP
O = makePlayer('O')
X = makePlayer('X')
players = [O, X]
print(X.name)
print(O.name)

board = makeBoard(9)
pointer = makePointer(9)
board.createBoard()
board.printBoard(players[0], pointer)


index = 0
try:
    while True:
        #CHECKS IF BUTTON IS PRESSED
        if (GPIO.input(11) == 1):
            print("down")
            time.sleep(0.1)
            pointer.setPosition(11, players[index], board)
            board.printBoard(players[index], pointer)
            while (GPIO.input(11) == 1):
                pass
        elif (GPIO.input(13) == 1):
            print("left")
            time.sleep(0.1)
            pointer.setPosition(13, players[index], board)
            board.printBoard(players[index], pointer)
            while (GPIO.input(13) == 1):
                pass
        elif (GPIO.input(15) == 1):
            print("up")
            time.sleep(0.1)
            pointer.setPosition(15, players[index], board)
            board.printBoard(players[index], pointer)
            while (GPIO.input(15) == 1):
                pass
        elif (GPIO.input(16) == 1):
            print("ok")
            time.sleep(0.1)
            pointer.setPosition(16, players[index], board)
            board.printBoard(players[index], pointer)
            board.winnerControl(players[index])
            index ^= 1
            while (GPIO.input(16) == 1):
                pass
        elif (GPIO.input(18) == 1):
            print("right")
            time.sleep(0.1)
            pointer.setPosition(18, players[index], board)
            board.printBoard(players[index], pointer)
            while (GPIO.input(18) == 1):
                pass
        else:
            pass
# Bör köras varje gång, ställer tillbaka alla pins till default, denna körs
#om man trycker ctrl+C
finally:
    GPIO.cleanup()

    

    
