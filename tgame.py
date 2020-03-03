import random


class Game():
    """
    It contains board initial details
    """

    def __init__(self):
        """
        board,successcombinations value initial
        """
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.gameend = False
        self.successCombinations = (
        (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.move=-1
        self.nodes=0

    def drawBoard(self):
        """
        To show the current board status
        """
        print('|', self.board[0], '|', self.board[1], '|', self.board[2], '|')
        print('|', self.board[3], '|', self.board[4], '|', self.board[5], '|')
        print('|', self.board[6], '|', self.board[7], '|', self.board[8], '|')
        print()


class ComputerPlayer():
    """
    It is used for auto movement in board
    """

    def __init__(self):
        pass

    def evaluateBoardResult(self,argboard):
        """
        Check the win strategy
        """

        for a in self.successCombinations:
            if argboard[a[0]] == argboard[a[1]] == argboard[a[2]] == 'O':
                return 1
            if argboard[a[0]] == argboard[a[1]] == argboard[a[2]] == 'X':
                return -1

        return 0

    def getScore(self,board, depth):
        """
        Get the score in the tree for the depth
        """
        if self.evaluateBoardResult(board) == 1:
            return 10 - depth
        elif self.evaluateBoardResult(board) == -1:
            return depth - 10
        else:
            return 0

    def checkBoardFreeSpace(self,board):
        """
                Decide the board have free space or not
        """
        for pos in board:
            if pos == ' ':
                return 1
        return 0

    def minimax(self,board, turn, depth):
        """
        minimax alogorithm to find the best move in pattern single player
        """

        if self.evaluateBoardResult(board) == 0 and self.checkBoardFreeSpace(board) == 0:
            return self.getScore(board, depth)

        moves = list()
        scores = list()
        self.nodes += 1
        for square, pos in enumerate(board):
            if pos == ' ':
                newboard = board.copy()
                if turn==-1:
                    newboard[square] = 'X'
                elif turn==1:
                    newboard[square] = 'O'

                moves.append(square)

                if self.evaluateBoardResult(newboard) in [1, -1] or self.checkBoardFreeSpace(newboard) == 0:
                    self.move = square
                    return self.getScore(newboard, depth)
                scores.append(self.minimax(newboard, turn * -1, depth + 1))
        # print(depth)
        # print(turn)
        # print(scores)
        # print(self.nodes)
        if turn == 1:
            self.move = moves[scores.index(max(scores))]
            return max(scores)
        elif turn == -1:
            self.move = moves[scores.index(min(scores))]
            return min(scores)

    def makeMove(self, argboard, letter, move):
        """
        move the value into given position
        """
        argboard[move] = letter

    def getBoardCopy(self, argboard):
        """
        Make copy from original board
        """
        dupeBoard = []
        for i in argboard:
            dupeBoard.append(i)
        return dupeBoard

    def isSpaceFree(self, argboard, move):
        """
        Decide the given position is occupied or not
        """
        return argboard[move] == ' '

    def isNumberFree(self, argboard, num):
        """
        Decide given value exists or not in board
        """
        return argboard.count(num) == 0

    def chooseRandomMoveFromList(self, movesList, numberList):
        """
        Get random position and to be filled value by random choice
        """
        possibleMoves = movesList
        possibleNumbers = numberList

        pos = None
        num = None

        if len(possibleMoves) != 0:
            pos = random.choice(possibleMoves)
        if len(possibleNumbers) != 0:
            num = random.choice(possibleNumbers)
        return pos, num

    def isWinner(self, argboard, argletter):
        """
        Check the win status for pattern based board
        """
        for a in self.successCombinations:
            if argboard[a[0]] == argboard[a[1]] == argboard[a[2]] == argletter:
                return True

    def isWinnerNumber(self, argboard):
        """
        Check the win status for number based board, by summing
        """
        for a in self.successCombinations:
            c1 = int(argboard[a[0]]) if argboard[a[0]] != ' ' else 0
            c2 = int(argboard[a[1]]) if argboard[a[1]] != ' ' else 0
            c3 = int(argboard[a[2]]) if argboard[a[2]] != ' ' else 0
            if c1 + c2 + c3 == 15:
                return True

    def getAutoMove(self, board, autoplayercontent, playercontent):
        """
        get next move position for pattern and get next move and value for number pattern
        1.Find empty place
        2.To check win strategy for player by applying own value, and get the position and corresponding
         number value
        3.To check lose strategy for player by applying opposite value, and get the position and
        fill random number value to avoid lose
        4.Find the corner position and to be filled number randomly
        5.Find the number to be filled in center place by random choice
        6.Find the side position and to be filled number randomly
        """

        emptyPlace = [ind for ind in range(0, 9) if self.isSpaceFree(board, ind)]

        for i in emptyPlace:
            copyboard = self.getBoardCopy(board)
            for autocontent in autoplayercontent:
                self.makeMove(copyboard, autocontent, i)
                if isinstance(autocontent, int):
                    if self.isWinnerNumber(copyboard):
                        return i, autocontent
                else:
                    if self.isWinner(copyboard, autocontent):
                        return i, autocontent

        for i in emptyPlace:
            copyboard = self.getBoardCopy(board)
            for playcontent in playercontent:
                self.makeMove(copyboard, playcontent, i)
                if isinstance(playcontent, int):
                    if self.isWinnerNumber(copyboard):
                        return i, random.choice(autoplayercontent)
                else:
                    if self.isWinner(copyboard, playcontent):
                        return i, random.choice(autoplayercontent)

        cornerAvailable = [ind for ind in [0, 2, 6, 8] if ind in emptyPlace]
        move, val = self.chooseRandomMoveFromList(cornerAvailable, autoplayercontent)
        if move != None:
            return move, val

        if self.isSpaceFree(board, 4):
            return 4, autoplayercontent

        sideAvailable = [ind for ind in [1, 3, 5, 7] if ind in emptyPlace]
        return self.chooseRandomMoveFromList(sideAvailable, autoplayercontent)

    def choosePositionNumberAuto(self, board):
        """
        Get the position for pattern game
        """
        """
        autoplayercontent = ['O']
        playercontent = ['X']
        pos, val = self.getAutoMove(board, autoplayercontent, playercontent)
        print(pos + 1)
        return pos
        """
        self.minimax(board,1,0)
        return self.move

    def choosePositionValueAuto(self, board):
        """
        Get the position and corresponding to be filled value for number game
        """
        autoplayercontent = [2, 4, 6, 8]
        playercontent = [1, 3, 5, 7, 9]
        for i in range(9):
            if board[i] in autoplayercontent:
                autoplayercontent.remove(board[i])
            if self.board[i] in playercontent:
                playercontent.remove(board[i])

        pos, val = self.getAutoMove(board, autoplayercontent, playercontent)
        # print(pos + 1, val)
        return pos, val


class PatternMode(Game, ComputerPlayer):

    def __init__(self):
        """
        Player 1/2 place filled value
        """
        super().__init__()
        self.fillPattern = {'Player 1': 'X', 'Player 2': 'O'}

    def play(self, playerno, isAuto=False):
        """
        Fill the value in position
        """
        if isAuto:
            pos = self.choosePositionNumberAuto(self.board.copy())
        else:
            pos = self.choosePositionNumber()
        if self.board[pos] == "X" or self.board[pos] == "O":
            print("\nYou should select correct position number. Try again")
            self.play(playerno, isAuto)
        else:
            self.board[pos] = self.fillPattern[playerno]

    def choosePositionNumber(self):
        """
        Get the place position from player for next move
        """
        while True:
            while True:
                item = input()
                try:
                    item = int(item)
                    item -= 1
                    if item in range(0, 9):
                        return item
                    else:
                        print("\nThis position is not on the board. Try again")
                        continue
                except ValueError:
                    print("\nThis is not a number. Try again")
                    continue

    def checkBoardResult(self, playerno):
        """
        Check the game result win,draw
        board Placeholder by default has single space value
        """

        for a in self.successCombinations:
            if self.board[a[0]] == self.board[a[1]] == self.board[a[2]] == self.fillPattern[playerno]:
                print("{} Won the game! Congrats! \n".format(playerno))
                return True

        filledplacecount = 0
        for a in range(9):
            if self.board[a] == "X" or self.board[a] == "O":
                filledplacecount += 1
            if filledplacecount == 9:
                print("The game ends in a Draw\n")
                return True


class NumberMode(Game, ComputerPlayer):

    def __init__(self):
        """
        Set the Player 1/2 valid values
        """
        super().__init__()
        self.fillPattern = {'Player 1': (1, 3, 5, 7, 9), 'Player 2': (2, 4, 6, 8)}

    def play(self, playerno, isAuto=False):
        """
        Fill the board place
        """
        if isAuto:
            pos, val = self.choosePositionValueAuto(self.board.copy())
        else:
            pos, val = self.choosePositionValue()
        if self.board[pos] != ' ' or val not in self.fillPattern[playerno]:
            print("\nYou should select correct both position list and the value list{}. Try again"
                  .format(self.fillPattern[playerno]))
            self.play(playerno, isAuto)
        else:
            self.board[pos] = val

    def choosePositionValue(self):
        """
        get the position and value to fill in the board
        """
        while True:
            while True:
                inp = input()

                try:
                    inp = inp.strip()
                    if inp.find(' ') == -1:
                        print("\n Placeholder and Place value should be separated by space during input given.")
                        continue
                    a, b = inp.split(' ')
                    a = int(a)
                    a -= 1
                    b = int(b)

                    if a in range(0, 9) and b in range(1, 10) and b not in self.board:
                        return a, b
                    else:
                        print("\nThis position is not on the board or value is already available in board. Try again")
                        continue
                except ValueError:
                    print("\nThis is not a number. Try again")
                    continue

    def checkBoardResult(self, playerno):
        """
        Check the game result win,draw
        board Placeholder by default has single space value
        """

        for a in self.successCombinations:
            c1 = int(self.board[a[0]]) if self.board[a[0]] != ' ' else 0
            c2 = int(self.board[a[1]]) if self.board[a[1]] != ' ' else 0
            c3 = int(self.board[a[2]]) if self.board[a[2]] != ' ' else 0
            if c1 + c2 + c3 == 15:
                print(c1, c2, c3)
                print("{} Won the game! Congrats!\n".format(playerno))
                return True

        # Verify all placeholder filled or not, decide draw
        filledplacecount = 0
        for a in range(9):
            if self.board[a] != ' ':
                filledplacecount += 1
            if filledplacecount == 9:
                print("The game ends in a Draw\n")
                return True


class PatternGame(PatternMode):
    """
        This is for Pattern based game , both double and single player
        when Row(horizontal,vertical,diagonal) contains same value either X or O,won, if not draw
        Player1 - (X)
        Player2 - (O)
    """

    def __init__(self, isAuto):
        super().__init__()
        self.isAuto = isAuto

    def start(self):
        """
                gameend initially False, once game get results, gameend will be True
        """
        while not self.gameend:
            self.drawBoard()
            self.gameend = self.checkBoardResult("Player 2")
            if self.gameend == True:
                break

            print("Player 1 choose where to place a 'Cross' in the board...")
            self.play("Player 1")
            print()
            self.drawBoard()
            self.gameend = self.checkBoardResult("Player 1")
            if self.gameend == True:
                break

            # Decide Player 2 either Person or Computer
            if self.isAuto:
                print("Player 2 is automatically choosing where to place a 'Nought'...")
            else:
                print("Player 2 choose where to place a 'Nought' in the board...")
            self.play("Player 2", self.isAuto)
            print()


class NumberGame(NumberMode):
    """
    This is for Number based game , both double and single player
    when Row(horizontal,vertical,diagonal) addition is 15,won, if not draw
    Player1 - (1,3,5,7,9)
    Player2 - (2,4,6,8)
    """

    def __init__(self, isAuto=False):
        super().__init__()
        self.isAuto = isAuto

    def start(self):
        """
        gameend initially False, once game get results, gameend will be True
        """
        while not self.gameend:
            self.drawBoard()
            self.gameend = self.checkBoardResult("Player 2")
            if self.gameend == True:
                break

            print("Player 1 choose position and value where to place and "
                  "what to put like 1 3 (Space is the input divider)... ")
            self.play("Player 1")
            print()
            self.drawBoard()
            self.gameend = self.checkBoardResult("Player 1")
            if self.gameend == True:
                break
            # Decide Player 2 either Person or Computer
            if self.isAuto:
                print(
                    "Player 2 (Computer) is automatically choosing the position and value "
                    "where to place and what to put like 2 6 (Space is the input divider)... ")
            else:
                print("Player 2 choose position and value where to place and what to put... ")
            self.play("Player 2", self.isAuto)
            print()


def main():
    gameMode = input("Please choose the Game Mode either 'Pattern' or 'Number'...")
    playerMode = input("Please choose the Player mode either 'Double' or 'Single'...")

    # isAuto flag for player2 either person or computer
    gameMode = gameMode.lower()
    playerMode = playerMode.lower()
    if gameMode == 'pattern' and playerMode == 'double':
        # Pattern based person vs person game
        gameone = PatternGame(isAuto=False)
        gameone.start()
    elif gameMode == 'pattern' and playerMode == 'single':
        # Pattern based person vs computer game
        gametwo = PatternGame(isAuto=True)
        gametwo.start()
    elif gameMode == 'number' and playerMode == 'double':
        # Number based person vs person game
        gamethree = NumberGame(isAuto=False)
        gamethree.start()
    elif gameMode == 'number' and playerMode == 'single':
        # Number based person vs computer game
        gamefour = NumberGame(isAuto=True)
        gamefour.start()
    else:
        print('You are exiting the game as selected game mode or player mode is not correct.')


if __name__ == '__main__':
    main()
