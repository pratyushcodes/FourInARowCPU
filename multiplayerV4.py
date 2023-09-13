def multiPlayerRunning():
    import pygame
    import numpy as np
    import time
    import sys

    pygame.init() # initialize or start pygame
    SQ_SIZE = 86 #length and the width of the square
    ROWS = 7
    COLUMNS = 7
    width = SQ_SIZE*ROWS
    height = SQ_SIZE*COLUMNS
    SCREEN = pygame.display.set_mode((width,height)) # make screen
    BLUE = (0, 0, 255) # blue color will be given once parameter is passed
    BLACK = (0, 0, 0) # black color will be given once parameter is passed
    RED = (255, 0, 0) # red color will be given once parameter is passed
    YELLOW = (255, 225, 0) # yellow color will be given once parameter is passed
    RECT = (0, SQ_SIZE, width, height - SQ_SIZE) # height needs to subtract SQ_SIZE
    RADIUS = int((SQ_SIZE/2)-5)
    STARTING_WIDTH = (SQ_SIZE/2)
    STARTING_HEIGHT = int(SQ_SIZE + (SQ_SIZE/2))


    from pygame import mixer
    bgMusic = 'mixkit-medieval-win.wav'  # downloaded from mixkit
    mixer.init()
    mixer.music.load(bgMusic)
    # mixer.music.play()


    #drawing the playing board
    def drawBoard():
        pygame.draw.rect(SCREEN,BLUE,RECT)
        for j in range(6):
            for i in range(7):
                pygame.draw.circle(SCREEN, BLACK, ((STARTING_WIDTH + SQ_SIZE*i), (STARTING_HEIGHT + SQ_SIZE*j)),RADIUS)
        pygame.display.update()

    #simulates dropping
    def simulateDropping(color,row,column):
        for each_row in range(row):
            pygame.draw.circle(SCREEN, color, ((STARTING_WIDTH + SQ_SIZE * column), (STARTING_HEIGHT + SQ_SIZE * each_row)),
                               RADIUS)
            pygame.display.update()
            time.sleep(0.2)
            pygame.draw.circle(SCREEN, BLACK, ((STARTING_WIDTH + SQ_SIZE * column), (STARTING_HEIGHT + SQ_SIZE * each_row)),
                               RADIUS)
            pygame.display.update()

    #drawing the piece
    def dropPiece(board,row,column,piece):
        if piece==1:
            color = RED
        elif piece==2:
            color = YELLOW

        board[row][column]=piece
        print(board)
        dropping = simulateDropping(color,row,column)
        pygame.draw.circle(SCREEN, color, ((STARTING_WIDTH + SQ_SIZE * column), (STARTING_HEIGHT + SQ_SIZE * row)), RADIUS)
        pygame.display.update()

    #start moving / board array
    def makePlayBoard():
        board = np.zeros((ROWS-1,COLUMNS),int)
        print(board)
        return board

    # this function make sures that which row the piece will be put in when it's dropped
    def getRow(board,column):
        for row in range(ROWS-1):
            if board[row][column]==0:
                pass
            elif board[row][column]==1:
                row = row - 1
                return row
            elif board[row][column]==2:
                row = row - 1
                return row
        return row

    # this function makes sure that the column is available for the person to drop the piece or else
    # they have to move somewhere else
    def checkAvailability(board, column):
        if board[0][column]==0:
            return True
        else:
            return False

    #this function makes sure that once a player wins by getting 4 in a row horizontally, the borders flash
    def flashHorizontalCircles(row,column):
        for i in range(4):
            pygame.draw.circle(SCREEN, BLACK, ((STARTING_WIDTH + SQ_SIZE * (column+i)), (STARTING_HEIGHT + SQ_SIZE * row)),
                               RADIUS,width=5, draw_top_right=True, draw_top_left=True, draw_bottom_left=True, draw_bottom_right=True)

    #this function makes sure that once a player wins by getting 4 in a row vertically, the borders flash
    def flashVerticalCircles(row,column):
        for i in range(4):
            pygame.draw.circle(SCREEN, BLACK,
                               ((STARTING_WIDTH + SQ_SIZE * column), (STARTING_HEIGHT + SQ_SIZE * (row+i))),
                               RADIUS,width=5, draw_top_right=True, draw_top_left=True, draw_bottom_left=True, draw_bottom_right=True)

    #this function makes sure that one a player wins by getting 4 in a row postive diagonal slope, the borders flash
    def flashDiagonalCirclesPositive(row,column):
        for i in range(4):
            pygame.draw.circle(SCREEN, BLACK, ((STARTING_WIDTH + SQ_SIZE * (column+i)), (STARTING_HEIGHT + SQ_SIZE * (row-i))),
                               RADIUS,width=5, draw_top_right=True, draw_top_left=True, draw_bottom_left=True, draw_bottom_right=True)

    #this function makes sure that one a player wins by getting 4 in a row negative diagonal slope, the borders flash
    def flashDiagonalCirclesNegative(row,column):
        for i in range(4):
            pygame.draw.circle(SCREEN, BLACK, ((STARTING_WIDTH + SQ_SIZE * (column+i)), (STARTING_HEIGHT + SQ_SIZE * (row+i))),
                               RADIUS,width=5, draw_top_right=True, draw_top_left=True, draw_bottom_left=True, draw_bottom_right=True)

    # this function makes sure that either player 1 or 2 will win the game if they get 4 in a row horizontally
    def horizontalWinningMove(board, row, column):
        for column in range(COLUMNS-3):
            if board[row][column]==1 and board[row][column+1]==1 \
            and board[row][column+2]==1 and board[row][column+3]==1:
                flashHorizontalCircles(row,column)
                return True
            elif board[row][column]==2 and board[row][column+1]==2 \
            and board[row][column+2]==2 and board[row][column+3]==2:
                flashHorizontalCircles(row, column)
                return True

    # this function makes sure that either player 1 or 2 will win the game if they get 4 in a row vertically
    def verticalWinningMove(board, row, column):
        for row in range(ROWS-4):
            if board[row][column] == 1 and board[row+1][column] == 1 \
            and board[row+2][column] == 1 and board[row+3][column] == 1:
                flashVerticalCircles(row, column)
                return True
            elif board[row][column]==2 and board[row+1][column]==2 \
            and board[row+2][column]==2 and board[row+3][column]==2:
                flashVerticalCircles(row,column)
                return True

    # this functions makes sure that either player 1 or 2 will win the game if they get 4 in a row diagonally
    def diagonalWinningMove(board, row, column):
        #check for negative slope
        for column in range(COLUMNS-3):
            for row in range(ROWS-4):
                if board[row][column] == 1 and board[row + 1][column+1] == 1 \
                and board[row + 2][column+2] == 1 and board[row + 3][column+3] == 1:
                    flashDiagonalCirclesNegative(row, column)
                    return True
                elif board[row][column] == 2 and board[row + 1][column + 1] == 2 \
                and board[row + 2][column + 2] == 2 and board[row + 3][column + 3] == 2:
                    flashDiagonalCirclesNegative(row, column)
                    return True

        #check for positive slope
        for column in range(COLUMNS-3):
            for row in range(ROWS-2,ROWS-5, -1):
                if board[row][column] == 1 and board[row-1][column+1] == 1 \
                and board[row-2][column+2] == 1 and board[row-3][column+3] == 1:
                    flashDiagonalCirclesPositive(row, column)
                    return True
                elif board[row][column] == 2 and board[row-1][column+1] == 2 \
                and board[row-2][column+2] == 2 and board[row-3][column+3] == 2:
                    flashDiagonalCirclesPositive(row, column)
                    return True

    # *** Whenever we want to print, we can call this board now that it's a function
    board = makePlayBoard() # global variable

    # end moving
    running = True

    drawBoard()
    count = 0
    piece=1
    while running == True and count<42:
        # this makes sure every move is captured while program is running
        events = pygame.event.get()
        for event in events:
        # for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                # pygame.display.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                print(event.key)
                if event.key==27:   # Esc = 27
                    running=False

            cursor = pygame.mouse.get_pos()
            column = cursor[0] // SQ_SIZE
            if event.type == pygame.MOUSEBUTTONDOWN:
                availability = checkAvailability(board, column)
                if availability == False:
                    continue
                row = getRow(board, column)
                dropPiece(board, row, column, piece)
                count = count + 1
                print(count)
                horizontalWinner = horizontalWinningMove(board, row, column)
                verticalWinner = verticalWinningMove(board, row, column)
                diagonalWinner = diagonalWinningMove(board, row, column)
                pygame.display.update()
                if horizontalWinner == True or verticalWinner == True or diagonalWinner == True:
                    mixer.music.play()
                    print("Congrats Player",piece, "you win!")
                    time.sleep(5)
                    running = False
                    break
                elif count==42:
                    print("Game Draw")
                    time.sleep(5)
                    running = False
                    break
                piece = piece % 2 + 1



        # makes sure top row is blank
        pygame.draw.rect(SCREEN, BLACK, (0, 0, width, SQ_SIZE))

        #follow mouse with red or yellow circle
        if piece==1:
            red_piece = pygame.draw.circle(SCREEN, RED, (cursor[0],SQ_SIZE/2), RADIUS)
        elif piece==2:
            yellow_piece = pygame.draw.circle(SCREEN, YELLOW, (cursor[0],SQ_SIZE/2),RADIUS)
        pygame.display.update()


    # pygame.display.update()
    # time.sleep(20)
    # pygame.event.wait(25)

if __name__ == "__main__":
    print(__name__)
    multiPlayerRunning()
