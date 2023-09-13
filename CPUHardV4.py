def cpuHard():
    import pygame
    import numpy as np
    import time
    import sys
    import random

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
    print(COLUMNS//2)
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
            print('row',row)
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

    # set scoring values
    def scoringValues(window, piece):
        score = 0
        oppositePiece = PLAYER

        if piece==PLAYER:
            oppositePiece=CPU


        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(0) == 1:
            score += 10
        elif window.count(piece) == 2 and window.count(0) == 2:
            score += 1

        if window.count(oppositePiece) == 3 and window.count(0)==1:
            score -= 90
        return score


    # for future move simulation on temp board
    def dropPieceCalc(board,row,column,piece):
        board[row][column]=piece


    def scoringPosition(board,piece):
        ## Scoring Position
        score = 0

        center_array = [int(i) for i in list(board[:, COLUMNS // 2])]
        print('center array', center_array)
        center_array = center_array[2:6]  # sub array bottom 4 rows
        print('center array 1', center_array)
        center_array = center_array[::-1]  # reverse
        print('center array 2', center_array)
        center_count = center_array.count(piece)
        # print('center_array: ',center_array)
        score += center_count * 6

        # Starting row 5 to 0
        # this is for horizontal winner
        for row in range(ROWS-2, -1, -1):
            print('row',row)
            row_array = [int(i) for i in list(board[row,:])]
            for column in range(COLUMNS - 3):
                window = row_array[column:column+4]
                # print(window)
                # print('row', row)
                # print(window.count(1))
                score += scoringValues(window, piece)
                # print("Score is",score)

        #this is for vertical winner
        for column in range(7):
            col_array = [int(i) for i in list(board[:,column])]
            # print('row array', row_array)
            for row in range(ROWS - 4):
                window = col_array[row:row + 4]
                # print(window)
                # print('row', row)
                # print(window.count(1))
                score += scoringValues(window, piece)

        # this is for negative diagoal winner
        for c in range(-2, 4):
            neg_diag_array = board.diagonal(c)
            neg_diag_array = [int(i) for i in list(neg_diag_array[:])]
            for column in range(len(neg_diag_array) - 3):
                window = neg_diag_array[column:column + 4]
                print(window)
                # print('row', row)
                # print(window.count(1))
                score += scoringValues(window, piece)
                # print("Score is",score)

        # this is for positive diagoal winner
        for c in range(-2, 4):
            pos_diag_array = np.flipud(board).diagonal(c)
            pos_diag_array = [int(i) for i in list(pos_diag_array[:])]

            for column in range(len(pos_diag_array) - 3):
                window = pos_diag_array[column:column + 4]
                print(window)
                # print('row', row)
                # print(window.count(1))
                score += scoringValues(window, piece)
                # print("Score is",score)

        return score

    #get array of valid locations
    def get_valid_locations(board):
        valid_locations = []
        for column in range(COLUMNS):
            if checkAvailability(board,column):
                valid_locations.append(column)
        return valid_locations

    def pick_best_move(board,piece):
        bestScore = -10000000000000
        valid_locations = get_valid_locations(board)
        bestColumn = random.choice(valid_locations)
        for column in valid_locations:
            row = getRow(board,column)
            # print('row', row)
            temp_board = board.copy()
            dropPieceCalc(temp_board,row,column,piece)
            score = scoringPosition(temp_board,piece)
            if score > bestScore:
                bestScore = score
                bestColumn = column
        return bestColumn



    # end of minimax





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
    CPU = 1
    PLAYER = 2
    piece=CPU

    piece = random.randint(1, 2)


    while running == True and count<42:
        # this makes sure every move is captured while program is running

        if piece == CPU and running:
            # column = random.randint(0,COLUMNS-1)
            column  = pick_best_move(board, piece)

            availability = checkAvailability(board, column)
            if availability == False:
                continue
            row = getRow(board, column)

            dropPiece(board, row, column, piece)
            count = count + 1
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



        events = pygame.event.get()
        for event in events:
        # for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                # pygame.display.quit()
                sys.exit()

            if event.type==pygame.KEYDOWN:
                # print(event.key)
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

                scoringPosition(board, piece)
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
    # print(__name__)
    cpuHard()
