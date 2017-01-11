"""Function for trollpy."""
from ChessRules import ChessRules

class ChessGUI_text:
    def __init__(self):
        self.Rules = ChessRules()

    def Draw(self,board):
        print "    c0   c1   c2   c3   c4   c5   c6   c7 "
        print "  ----------------------------------------"
        for r in range(8):
            print "r"+str(r)+"|",
            for c in range(8):
                if board[r][c] != 'e':
                    print  str(board[r][c]), "|",
                else:
                    print "   |",
                if c == 7:
                    print #to get a new line
            print "  ----------------------------------------"

    def EndGame(self, board):
        self.Draw(board)

    def GetPlayerInput(self, board, color, tup):
        print(tup)
        fromTuple = self.GetPlayerInput_SquareFrom(board, color, tup[0])
        if fromTuple:
            toTuple = self.GetPlayerInput_SquareTo(board, color, fromTuple, tup[1])
            if toTuple:
                return (fromTuple, toTuple)
        return False

    def GetPlayerInput_SquareFrom(self,board,color, tup):
        ch = "w"
        cmd_r = tup[0]
        cmd_c = tup[1]
        good_square = True

        if (board[cmd_r][cmd_c] == 'e'):
            print "  Nothing there!"
            good_square = False
        elif (ch not in board[cmd_r][cmd_c]):
            print "  That's not your piece!"
            good_square = False
        elif self.Rules.GetListOfValidMoves(board, color, (cmd_r, cmd_c)) == []:
            print "  No valid moves for that piece!"
            good_square = False

        if good_square:
            return (cmd_r, cmd_c)
        else:
            return False


    def GetPlayerInput_SquareTo(self,board,color,fromTuple, toTuple):
        validMoveList = self.Rules.GetListOfValidMoves(board, color, fromTuple)
        print "List of valid moves for piece at", fromTuple, ": ", validMoveList

        if not toTuple in validMoveList:
            print "  Invalid move!"
            return False
        return toTuple


    def PrintMessage(self,message):
        print message



if __name__ == "__main__":
    from ChessBoard import ChessBoard

    cb = ChessBoard(0)

    gui = ChessGUI_text()
    gui.Draw(cb.GetState())