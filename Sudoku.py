#    15-112: Principles of Programming and Computer Science
#    Term Project: Sudoku
#    Name      : Noor Aljaber
#    AndrewID  : naljaber

#    
#    
#    

import math
from tkinter import *


def areLegalValues(a):
    n = len(a)
    i = int(math.sqrt(n))

    if i*i == n:
        for x in a:
            if (x < 0) or (x > n) or (type(x) != int):
                return False
            if (x != 0) and (a.count(x) != 1):
                return False
        return True   
    return False
            
                
def isLegalRow(board, row):
    for i in range(len(board)):
        if (i == row) and (areLegalValues(board[i])):
            return True
    return False


def isLegalCol(board, col):
    colValues = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if j == col:
                colValues.append(board[i][j])
    return areLegalValues(colValues)


def isLegalBlock(board, block):
    blockValues = []
    i = int(math.sqrt(len(board)))

    if block == 0:
        for x in range(i):
            for y in range(i):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)
    
    elif block == 1:
        for x in range(i):
            for y in range(i,i*2):
                blockValues.append(board[x][y]) 
        return areLegalValues(blockValues)
    
    elif block == 2:
        for x in range(i):
            for y in range(i*2,len(board)):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)

    elif block == 3:
        for x in range(i, len(board)-i):
            for y in range(i):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)
    
    elif block == 4:
        for x in range(i, len(board)-i):
            for y in range(i, len(board)-i):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)

    elif block == 5:
        for x in range(i, len(board)-i):
            for y in range(i*2, len(board)):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)

    elif block == 6:
        for x in range(i*2, len(board)):
            for y in range(i):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)

    elif block == 7:
        for x in range(i*2, len(board)):
            for y in range(i, len(board)-i):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)
    
    elif block == 8:
        for x in range(i*2, len(board)):
            for y in range(i*2, len(board)):
                blockValues.append(board[x][y])
        return areLegalValues(blockValues)


def isLegalSudoku(board):
    for i in range(len(board)):
        if not (isLegalRow(board,i) and isLegalCol(board, i) and isLegalBlock(board,i)):
            return False
    return True

def starterBoard():
    board = [ 
        [ 5, 3, 4, 6, 7, 8, 9, 1, 2],
        [ 6, 7, 2, 1, 9, 5, 3, 4, 8], 
        [ 1, 9, 8, 3, 4, 2, 5, 6, 7], 
        [ 8, 5, 9, 7, 6, 1, 4, 2, 3],
        [ 4, 2, 6, 8, 5, 3, 7, 9, 1],
        [ 7, 1, 3, 9, 2, 4, 8, 5, 6],
        [ 9, 6, 1, 5, 3, 7, 2, 8, 4],
        [ 2, 8, 7, 4, 1, 9, 6, 3, 5],
        [ 3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
    
    return board


#### Sudoku Animation ####

WIDTH = 400
HEIGHT = 400
SIZE = 3
MARGIN = 20

SQUARESIZE = min(WIDTH-2*MARGIN, HEIGHT-2*MARGIN)/(SIZE*SIZE)

outlined_rectangle = None
lastclickedCell = None
timeAllowed = 420


fillNumber_dict = {}

board = [ 
[ 5, 3, 4, 0, 7, 8, 9, 1, 2],
[ 0, 0, 2, 1, 0, 0, 0, 4, 0], 
[ 0, 9, 0, 3, 0, 2, 5, 0, 7], 
[ 8, 0, 0, 0, 6, 0, 4, 2, 3],
[ 0, 0, 6, 0, 0, 3, 7, 0, 0],
[ 7, 1, 0, 9, 0, 0, 8, 5, 0],
[ 0, 0, 1, 0, 3, 0, 0, 0, 0],
[ 0, 0, 0, 4, 0, 9, 6, 0, 5],
[ 3, 0, 5, 2, 0, 6, 0, 7, 0]
]

userEditable = []
for row in board:
    line = []
    userEditable.append(line)
    for c in row:
        if c == 0:
            line.append(True)
        else:
            line.append(False)


def minutesAndSeconds(secs):
    return (secs//60, secs % 60)

def timeStrToSeconds(s):
    m, s = s.split(':')
    m = int(m)
    s = int(s)
    return m * 60 + s
    
def setTimeRemaining(secsRemaining):
    m, s = minutesAndSeconds(secsRemaining) 
    timeStr = str(m) + ":" + str(s).rjust(2, '0')
    timeRemaining.set(timeStr)
    
    
def fillInBoard(board, canvas):
    for i in range(SIZE*SIZE):
        for j in range(SIZE*SIZE):
            number = board[i][j]
            x = MARGIN + 0.5*SQUARESIZE + j*SQUARESIZE
            y = MARGIN + 0.5*SQUARESIZE + i*SQUARESIZE
            if number != 0:
                canvas.create_text(x, y, text=str(number))
            
            
def getClickedCell(xclick, yclick):
    
    if xclick < MARGIN  or xclick > WIDTH-MARGIN or yclick < MARGIN or yclick > HEIGHT-MARGIN:
        return None
    else:
        x = xclick - MARGIN
        y = yclick - MARGIN
        i = 0
        j = 0
        while x > SQUARESIZE:
            x -= SQUARESIZE
            i += 1
        while y > SQUARESIZE:
            y -= SQUARESIZE
            j += 1
        
        return (j, i)

        
def returnToMenu():
    return
    
def pauseGame():
    return
    
def revealHint():
    return
    
def decreaseTime():
    timeStr = timeRemaining.get()
    timeInSeconds = timeStrToSeconds(timeStr)
    timeInSeconds -= 1

    setTimeRemaining(timeInSeconds)
    canvas.after(1000, decreaseTime)

def fillNumber(event):
    keypressed = event.char
    if '0' <= keypressed <= '9':
        if lastclickedCell != None:
            r, c = lastclickedCell
            if userEditable[r][c]:
                x = MARGIN + c * SQUARESIZE + 0.5 * SQUARESIZE
                y = MARGIN + r * SQUARESIZE + 0.5 * SQUARESIZE
                           
        
def outlineClickedCell(event):
    global outlined_rectangle 
    global lastclickedCell
    
    lastclickedCell = getClickedCell(event.x, event.y)
    if lastclickedCell == None:
        return
    r, c = lastclickedCell
    
    x1, y1 = (MARGIN + c * SQUARESIZE, MARGIN + r * SQUARESIZE)
    x2, y2 = (x1 + SQUARESIZE, y1 + SQUARESIZE)

    if outlined_rectangle != None:
        canvas.delete(outlined_rectangle)
    outlined_rectangle = canvas.create_rectangle(x1, y1, x2, y2, outline='red', width='3')
    
    
    
root = Tk()
timeRemaining = StringVar()
setTimeRemaining(timeAllowed)

leftFrame = Frame(root)
rightFrame = Frame(root)
leftFrame.pack(side=LEFT)
rightFrame.pack(side=LEFT, padx=50)
Button(rightFrame, text="Back to Menu", command=returnToMenu, height = 2, width = 15).pack()
Button(rightFrame, text="Pause", command=pauseGame, height = 2, width = 15).pack()
Button(rightFrame, text="Hint", command=revealHint, height = 2, width = 15).pack()
Label(rightFrame, textvariable=timeRemaining).pack()

canvas = Canvas(leftFrame, width=WIDTH, height=HEIGHT, background = "linen")
canvas.bind("<Button-1>", outlineClickedCell)
canvas.bind("<Any-KeyPress>", fillNumber)
canvas.pack()

for i in range(SIZE * SIZE+1):
    linewidth = 1
    if i % SIZE == 0:
        linewidth = 3
    
    canvas.create_line(MARGIN, i*SQUARESIZE+MARGIN, WIDTH-MARGIN, i*SQUARESIZE+MARGIN, width=linewidth)
    canvas.create_line(i*SQUARESIZE+MARGIN, MARGIN, i*SQUARESIZE+MARGIN, HEIGHT-MARGIN, width=linewidth)

    
fillInBoard(board, canvas)
root.after(1000, decreaseTime)
root.title("Sudoku")
root.mainloop()
