#    15-112: Principles of Programming and Computer Science
#    Term Project: Sudoku
#    Name      : Noor Aljaber
#    AndrewID  : naljaber

#    
#    
#  


import urllib.request
import json
from PIL import ImageTk
from PIL import Image as Img # tkinter also has Image class which clashes with this. https://shrtm.nu/mPuD
from tkinter import *
import math
from random import randint # to reveal hint square randomly
from datetime import datetime

USE_FIXED_GAME = False # True means use the small test board provided, False means download from internet

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
     
def isGameWon(board):
    if not isLegalSudoku(board):
        return False
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return False
    return True
    
def getBlockNumberFromRowCol(row, col):
    superRow = row // 3
    superCol = col // 3
    return superCol + 3 * superRow
    

############ taken from stackoverflow (sudoku solver)
def findNextCellToFill(grid, i, j):
    for x in range(i,9):
        for y in range(j,9):
            if grid[x][y] == 0:
                return x,y
    for x in range(0,9):
        for y in range(0,9):
            if grid[x][y] == 0:
                return x,y
    return -1,-1

def isValid(grid, i, j, e):
    rowOk = all([e != grid[i][x] for x in range(9)])
    if rowOk:
        columnOk = all([e != grid[x][j] for x in range(9)])
        if columnOk:
            # finding the top left x,y co-ordinates of the section containing the i,j cell
            secTopX, secTopY = 3 *(i//3), 3 *(j//3) #floored quotient should be used here. 
            for x in range(secTopX, secTopX+3):
                for y in range(secTopY, secTopY+3):
                    if grid[x][y] == e:
                        return False
            return True
    return False

def solveSudoku(grid, i=0, j=0):
    i,j = findNextCellToFill(grid, i, j)
    if i == -1:
        return True
    for e in range(1,10):
        if isValid(grid,i,j,e):
            grid[i][j] = e
            if solveSudoku(grid, i, j):
                return True
            # Undo the current cell for backtracking
            grid[i][j] = 0
    return False
############## end of borrowed code


def SudokuSolution(board):
    board_copy = [9 * [0] for i in range(9)]
    for i in range(9):
        for j in range(9):
            board_copy[i][j] = board[i][j]
            
    solveSudoku(board_copy)
    return board_copy
    
####
def getAllEmptyCellPositions(board):
    positions = []
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                positions.append((i, j))
    return positions


def chooseEmptyCellAtRandom(board):
    vacantCells = getAllEmptyCellPositions(board)
    if len(vacantCells) == 0:
        return None
    randomIdx = randint(0, len(vacantCells)-1)
    randomVacantCell = vacantCells[randomIdx]
    return randomVacantCell
    
    
def getAllIncorrectlyFilledEntries(board, solution):
    positions = []
    for i in range(9):
        for j in range(9):
            if board[i][j] and board[i][j] != solution[i][j]:
                positions.append((i, j))
                
    return positions
    
    
def chooseRandomIncorrectlyFilledEntry(board, solution):
    incorrectPositions = getAllIncorrectlyFilledEntries(board, solution)
    if len(incorrectPositions) == 0:
        return None
    randomIdx = randint(0, len(incorrectPositions)-1)
    incorrectCell = incorrectPositions[randomIdx]
    return incorrectCell
                          
####

def fetchGame(use_fixed):
    if use_fixed:
        board = [ 
        [ 5, 3, 4, 0, 7, 8, 9, 1, 2],
        [ 6, 7, 2, 1, 9, 5, 3, 4, 8], 
        [ 1, 9, 8, 3, 4, 2, 5, 6, 7], 
        [ 8, 5, 9, 7, 6, 0, 4, 2, 3],
        [ 4, 2, 6, 8, 5, 3, 7, 9, 1],
        [ 7, 1, 3, 9, 2, 4, 8, 5, 6],
        [ 9, 6, 1, 0, 3, 7, 2, 8, 4],
        [ 2, 8, 7, 4, 1, 9, 6, 3, 5],
        [ 3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]
        return board
    
    contents = urllib.request.urlopen("http://www.cs.utep.edu/cheon/ws/sudoku/new/?level=2&size=9").read().decode('ascii')

    game_dict = json.loads(contents)
    board = [[0] * 9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            board[i][j] = 0
    squares = game_dict['squares']
    
    for square in squares:
        x = square['x']
        y = square['y']
        value = square['value']
        board[x][y] = value
        
    return board
    

def userEditableCells(board):
    userEditable = [[False] * 9 for i in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                userEditable[i][j] = True
            else:
                userEditable[i][j] = False
    return userEditable
    

def minutesAndSeconds(secs):
    return (secs//60, secs % 60)

def timeStrToSeconds(s):
    m, s = s.split(':')
    m = int(m)
    s = int(s)
    return m * 60 + s

    
def topLeftAndBottomRightCoords(r, c):
    x1, y1 = (MARGIN + c * SQUARESIZE, MARGIN + r * SQUARESIZE)
    x2, y2 = (x1 + SQUARESIZE, y1 + SQUARESIZE)
    return ((x1, y1), (x2, y2))
    
def getClickedCell(data, xclick, yclick):
    m = data.MARGIN
    w = data.WIDTH
    h = data.HEIGHT
    ss = data.SQUARESIZE
    
    if xclick < m  or xclick > w-m or yclick < m or yclick > h-m:
        return None
    else:
        x = xclick - m
        y = yclick - m
        i = 0
        j = 0
        while x > ss:
            x -= ss
            i += 1
        while y > ss:
            y -= ss
            j += 1
        
        return (j, i)


# Updated Animation Starter Code
# from cmu 15/112 2019 Spring

####################################
# customize these functions
####################################

def init(data):
    data.startScreen = True
    data.WIDTH = 400
    data.HEIGHT = 400
    data.SIZE = 3
    data.MARGIN = 20
    data.SQUARESIZE = min(data.WIDTH-2*data.MARGIN, data.HEIGHT-2*data.MARGIN)/(data.SIZE*data.SIZE)
    
    data.gameRunning = True
    data.outlineRow = 0
    data.outlineCol = 0
    data.board = []
    data.solution = []
    data.userEditable = []
    data.fillNumber_dict = {}
    
    data.timeElapsed = StringVar() 
    data.messages = StringVar()
    data.showingIncorrectHint = False
    data.showingBlankHint = False
    data.hintTimeBegins = 0
    data.hintDuration = 2
    data.blankHintRow = -1
    data.blankHintCol = -1
    data.incorrectHintRow = -1
    data.incorrectHintCol = -1
    newGame(data)


def newGame(data):
    data.timeElapsed.set("00:00")
    data.board = fetchGame(USE_FIXED_GAME)
    data.solution = SudokuSolution(data.board)
    data.userEditable = userEditableCells(data.board)
    data.numHintsRemaining = 3
    data.fillNumber_dict.clear()
    
    
def moveOutlinedCellTo(data, r, c):
    data.outlineRow = r
    data.outlineCol = c  

def mousePressed(event, data):
    if isGameWon(data.board):
        return
    lastclickedCell = getClickedCell(data, event.x, event.y)
    if lastclickedCell == None:
        return
    else:
        data.outlineRow, data.outlineCol = lastclickedCell
    
def timerFired(data):
    if data.showingBlankHint or data.showingIncorrectHint:
        if datetime.now().timestamp() - data.hintTimeBegins > data.hintDuration:
            data.showingBlankHint = False
            data.showingIncorrectHint = False
            

def keyPressed(event, data):
    if isGameWon(data.board):
        return
    
    keypressed = event.char
    if '1' <= keypressed <= '9':
        r, c = data.outlineRow, data.outlineCol
        
        if data.userEditable[r][c]:
            data.board[r][c] = int(keypressed)
            legal = True

            if not isLegalRow(data.board, r):
                legal = False
                #message = "Row violation in row " + str(r)
                #data.messages.set(message)
                
            elif not isLegalCol(data.board, c):
                legal = False
                #message = "Column violation in column " + str(c)
                #data.messages.set(message)
            elif not isLegalBlock(data.board, getBlockNumberFromRowCol(r, c)):
                legal = False
                #message = "Block violation in block " + str(getBlockNumberFromRowCol(r, c))
                #data.messages.set(message)
                
            if not legal:
                data.board[r][c] = 0 # can change values in the board

        if isGameWon(data.board):
            data.won = True
            
    elif event.keysym in ['Left', 'Down', 'Right', 'Up']:
        r, c = data.outlineRow, data.outlineCol
        if event.keysym == 'Left' and c > 0:
            moveOutlinedCellTo(data, r, c-1)
        elif event.keysym == 'Right' and c < 9-1:
            moveOutlinedCellTo(data, r, c+1)
        elif event.keysym == 'Up' and r > 0:
            moveOutlinedCellTo(data, r-1, c)
        elif event.keysym == 'Down' and r < 9-1:
            moveOutlinedCellTo(data, r+1, c)


def drawGridLines(canvas, data):
    for i in range(9+1):
        linewidth = 1
        if i % 3 == 0:
            linewidth = 3
            
        m = data.MARGIN
        ss = data.SQUARESIZE
        w = data.WIDTH
        h = data.HEIGHT
        canvas.create_line(m, i*ss+m, w-m, i*ss+m, width=linewidth)
        canvas.create_line(i*ss+m, m, i*ss+m, h-m, width=linewidth)
            
            
def fillInBoard(canvas, data):
    def canvasCoordinatesForRowColumnCenter(i, j):
        x = data.MARGIN + 0.5*data.SQUARESIZE + j*data.SQUARESIZE
        y = data.MARGIN + 0.5*data.SQUARESIZE + i*data.SQUARESIZE
        return x, y
    def cornersOfSquare(i, j):
        x1 = data.MARGIN + j*data.SQUARESIZE
        y1 = data.MARGIN + i*data.SQUARESIZE
        x2 = x1 + data.SQUARESIZE
        y2 = y1 + data.SQUARESIZE
        return x1, y1, x2, y2
        
    for i in range(9):
        for j in range(9):
            number = data.board[i][j]
            x, y = canvasCoordinatesForRowColumnCenter(i, j)
            digit = ''
            if number != 0:
                digit = str(number)
            
            canvas.create_text(x, y, text=digit)
            if i == data.outlineRow and j == data.outlineCol:
                x1, y1, x2, y2 = cornersOfSquare(i, j)
                canvas.create_rectangle(x1, y1, x2, y2, outline = 'red', width=3)
                
    if data.showingBlankHint:
        x1, y1, x2, y2 = cornersOfSquare(data.blankHintRow, data.blankHintCol)
        canvas.create_rectangle(x1, y1, x2, y2, fill="yellow")
        x, y = canvasCoordinatesForRowColumnCenter(data.blankHintRow, data.blankHintCol)
        canvas.create_text(x, y, text=str(data.solution[data.blankHintRow][data.blankHintCol]))
        
    elif data.showingIncorrectHint:
        x1, y1, x2, y2 = cornersOfSquare(data.incorrectHintRow, data.incorrectHintCol)
        canvas.create_line(x1, y1, x2, y2, fill='blue', width=3)
        canvas.create_line(x1, y2, x2, y1, fill='blue', width=3)
        

def redrawAll(canvas, data):
    if isGameWon(data.board):
        canvas.create_image(data.WIDTH/2, data.HEIGHT/2, image=data.gameOverImg)
    else:
        drawGridLines(canvas, data)
        fillInBoard(canvas, data)
        
    
def revealIncorrectHint(data):
    if data.showingIncorrectHint or data.showingBlankHint:
        return # already showing
    else:
         
        incorrectlyFilledCell = chooseRandomIncorrectlyFilledEntry(data.board, data.solution)
        if incorrectlyFilledCell == None:
            data.messages.set("No incorrectly filled cells!")
            
        else:
            data.showingIncorrectHint = True
            data.incorrectHintRow, data.incorrectHintCol = incorrectlyFilledCell
            data.hintTimeBegins = datetime.now().timestamp()
    
def revealBlankHint(data):
    if data.showingIncorrectHint or data.showingBlankHint:
        return # already showing
    else:
        data.showingBlankHint = True
        data.blankHintRow, data.blankHintCol = chooseEmptyCellAtRandom(data.board)
        data.hintTimeBegins = datetime.now().timestamp()
        

####################################
# use the run function as-is
####################################

def run(width=400, height=400):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
        
    def updateTime(canvas, data):
        if not isGameWon(data.board):
            timeStr = data.timeElapsed.get()
            (m, s) = minutesAndSeconds(timeStrToSeconds(timeStr)+1)
            timeStr = str(m).zfill(2) + ":" + str(s).zfill(2)
            data.timeElapsed.set(timeStr)
            canvas.after(1000, updateTime, canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    data.gameOverImg = ImageTk.PhotoImage(Img.open("noor.png")) # source: shutterstock.com 
    canvas = Canvas(root, width=300, height=300)
    
    leftFrame = Frame(root)
    rightFrame = Frame(root)
    canvas.rightFrame = rightFrame
    canvas.rightFrame.pack_forget()
    leftFrame.pack(side=LEFT)
    rightFrame.pack(side=LEFT, padx=50)
    Button(rightFrame, text="Show blank Hint!", command=lambda: revealBlankHint(data), width=20, height = 2).pack()
    Button(rightFrame, text="Show incorrect Hint!", command=lambda: revealIncorrectHint(data), width=20, height = 2).pack()
    Button(rightFrame, text="Start new game", command=lambda:newGame(data), width=20, height = 2).pack()
    Label(rightFrame, textvariable=data.timeElapsed).pack()
    Label(rightFrame, textvariable=data.messages).pack()
    
    canvas = Canvas(leftFrame, width=data.width, height=data.height)
    
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    
    # set up events
    root.bind("<Button-1>", lambda event:
            mousePressedWrapper(event, canvas, data))
    canvas.focus_set()
    root.bind("<Key>", lambda event:
            keyPressedWrapper(event, canvas, data))
                            
    timerFiredWrapper(canvas, data)
    updateTime(canvas, data)
    # and launch the app
    root.title("Oh Sudoku")
    root.mainloop()  # blocks until window is closed

run(400, 400)
