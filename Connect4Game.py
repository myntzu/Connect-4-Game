import random
import copy
import sys

BOARDWIDTH = 0
levelN = 7      #Normal Level containing 7 columns x 6 rows
levelA = 9      #Advanced Level containing 9 columns x 6 rows
BOARDHEIGHT = 6
score = 5       #3points are given for every move player makes

global attempt #displays message according to number of attempts

select_level = int(input("Please select a level ['0 = Normal' or '1 = Advanced'] :"))    #promps player to select level before starting the game

if select_level == 1:   #if 1 is chosen ; Advance mode is given
    BOARDWIDTH = levelA
else:
    BOARDWIDTH = levelN #else player plays Normal mode


def main():
    """
    b = getNewBoard()
    b[6][5] = 'X'
    b[5][4] = 'X'
    b[4][3] = 'X'
    b[3][2] = 'X'
    drawBoard(b)
    print(isWinner(b, 'X'))

    sys.exit()
    """
    print()
    print('Let\'s Play Connect 4!')
    print()

    while True:
        count = 0
        humanTile, computerTile = enterHumanTile()
        turn = whoGoesFirst()   #prompts first turn i.e human/comp as player
        print('The %s player will go first.' % (turn))
        mainBoard = getNewBoard()

        while True:
            if turn == 'human':     #human plays first
                drawBoard(mainBoard)
                move = getHumanMove(mainBoard)
                makeMove(mainBoard, humanTile, move)
                count = count + 1
                if isWinner(mainBoard, humanTile):
                    winner = 'human'
                    break
                turn = 'computer'       #computer's turn to play
            else:
                drawBoard(mainBoard)
                print('The computer is thinking...')
                move = getComputerMove(mainBoard, computerTile)
                makeMove(mainBoard, computerTile, move)
                if isWinner(mainBoard, computerTile):
                    winner = 'computer' #computer as winner
                    break
                turn = 'human'          #human's turn again

            if isBoardFull(mainBoard):
                winner = 'tie'          #when both players' results are tied
                break

        drawBoard(mainBoard)
        print('Winner is: %s' % winner) #prints actual winner based on game result

        attempt = Message(count)        
        print("\nNumber of Attempts:",count) #prints the number of attempts taken by player
        print(attempt)                  #prints ending message

        playerScore = score*count
        print("\nYou've scored", playerScore, "points! Well done.")
        if not playAgain():
            break


def playAgain():
    # This function returns True if the player wants to play again, otherwise it returns False.
    print('Do you want to play again? (yes or no)')
    return input().lower().startswith('y')


def enterHumanTile():
    # Let's the human player type which tile they want to be.
    # Returns a list with the human player's tile as the first item, and the computer's tile as the second.
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

    # the first element in the tuple is the human player's tile, the second is the computer's tile.
    if tile == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']


def drawBoard(board):
    print()
    print(' ', end='')
    for x in range(1, BOARDWIDTH + 1):
        print(' %s  ' % x, end='')
    print()

    print('+---+' + ('---+' * (BOARDWIDTH - 1)))

    for y in range(BOARDHEIGHT):
        print('|   |' + ('   |' * (BOARDWIDTH - 1)))

        print('|', end='')
        for x in range(BOARDWIDTH):
            print(' %s |' % board[x][y], end='')
        print()

        print('|   |' + ('   |' * (BOARDWIDTH - 1)))

        print('+---+' + ('---+' * (BOARDWIDTH - 1)))


def getNewBoard():
    board = []
    for x in range(BOARDWIDTH):
        board.append([' '] * BOARDHEIGHT)
    return board


def getHumanMove(board):
    while True:
        print('Which column do you want to move on? (1-%s, or "quit" to quit game)' % (BOARDWIDTH))
        move = input()
        if move.lower().startswith('q'):
            sys.exit()
        if not move.isdigit():
            continue
        move = int(move) - 1
        if isValidMove(board, move):
            return move

def getComputerMove(board, computerTile):
    potentialMoves = getPotentialMoves(board, computerTile, 2)
    bestMoveScore = max([potentialMoves[i] for i in range(BOARDWIDTH) if isValidMove(board, i)])
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveScore:
            bestMoves.append(i)
    return random.choice(bestMoves)


def getPotentialMoves(board, playerTile, lookAhead):    #predicts player moves and makes it harder for player to win >:)
    if lookAhead == 0:
        return [0] * BOARDWIDTH

    potentialMoves = []

    if playerTile == 'X':
        enemyTile = 'O'
    else:
        enemyTile = 'X'

    # Returns (best move, average condition of this state)
    if isBoardFull(board):
        return [0] * BOARDWIDTH

    # Figure out the best move to make.
    potentialMoves = [0] * BOARDWIDTH
    for playerMove in range(BOARDWIDTH):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, playerMove):
            continue
        makeMove(dupeBoard, playerTile, playerMove)
        if isWinner(dupeBoard, playerTile):
            potentialMoves[playerMove] = 1
            break
        else:
            # do other player's moves and determine best one
            if isBoardFull(dupeBoard):
                potentialMoves[playerMove] = 0
            else:
                for enemyMove in range(BOARDWIDTH):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, enemyMove):
                        continue
                    makeMove(dupeBoard2, enemyTile, enemyMove)
                    if isWinner(dupeBoard2, enemyTile):
                        potentialMoves[playerMove] = -1
                        break
                    else:
                        results = getPotentialMoves(dupeBoard2, playerTile, lookAhead - 1)
                        potentialMoves[playerMove] += (sum(results) / BOARDWIDTH) / BOARDWIDTH
    return potentialMoves

def whoGoesFirst():
    # Randomly choose the player who goes first.
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'human'


def makeMove(board, player, column):
    for y in range(BOARDHEIGHT-1, -1, -1):
        if board[column][y] == ' ':
            board[column][y] = player
            return


def isValidMove(board, move):
    if move < 0 or move >= (BOARDWIDTH):
        return False

    if board[move][0] != ' ':
        return False

    return True


def isBoardFull(board):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == ' ':
                return False
    return True


def isWinner(board, tile):
    # check horizontal spaces
    for y in range(BOARDHEIGHT):
        for x in range(BOARDWIDTH - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True

    # check vertical spaces
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True

    # check (/) diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(3, BOARDHEIGHT):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check (\) diagonal spaces
    for x in range(BOARDWIDTH - 3):
        for y in range(BOARDHEIGHT - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True

    return False

def Message(count):
    if count < 10:
        message = "You have the talent!"
    elif count < 15:
        message = "Not too Bad"
    else:
        message = "You can do Better"
    return message


main()


