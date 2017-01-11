"""Chess game."""


import chess
import random


board = chess.Board()


def game():
    """Run the chess game."""
    while not board.is_game_over():
        print(board)
        move = input('your move: ')
        while chess.Move.from_uci(move) not in board.legal_moves:
            print('Not a legal move.')
        board.push_uci(move)
        print(board)
        troll_move = troll()
        print(troll_move)
        board.push(troll_move)


def troll():
    """Generate a move for the troll."""
    possible_moves = []
    for i in board.legal_moves:
        print(i)
        possible_moves.append(i)
    print(possible_moves)
    troll_move = random.randint(0, len(board.legal_moves))
    return possible_moves[troll_move]


if __name__ == '__main__':
    game()
