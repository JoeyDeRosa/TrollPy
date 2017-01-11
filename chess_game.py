"""Chess game."""


import chess
import random


board = chess.Board()


def game():
    """Run the chess game."""
    while True:
        print(board)
        print(board.fen())
        move = input('your move: ')
        while chess.Move.from_uci(move) not in board.legal_moves:
            print('Not a legal move.')
            move = input('your move: ')
        board.push_uci(move)
        if board.is_game_over():
            return 'You win.'
        print(board)
        print(board.fen())
        troll_move = troll()
        board.push(troll_move)
        if board.is_game_over():
            return 'You lose.'


def troll():
    """Generate a move for the troll."""
    moves = {
        'high_priority_moves': [],
        'med_priority_moves': [],
        'low_priority_moves': [],
    }
    moves = prioritize_troll_moves(moves)
    prefered_move_list = select_move_list(moves)
    troll_move = random.randint(0, len(prefered_move_list) - 1)
    return prefered_move_list[troll_move]


def prioritize_troll_moves(moves):
    """Return a dictionary of the trolls moves seperated by priority."""
    for move in board.legal_moves:
        if board.is_capture(move):
            if board.is_attacked_by(chess.WHITE, move.to_square):
                moves['med_priority_moves'].append(move)
            else:
                moves['high_priority_moves'].append(move)
        else:
            if board.is_attacked_by(chess.WHITE, move.to_square):
                moves['low_priority_moves'].append(move)
            else:
                moves['med_priority_moves'].append(move)
    return moves


def select_move_list(moves):
    """Return the list of moves with the highest priority for the troll to choose from."""
    if len(moves['high_priority_moves']) > 0:
        return moves['high_priority_moves']
    if len(moves['med_priority_moves']) > 0:
        return moves['med_priority_moves']
    return moves['low_priority_moves']


if __name__ == '__main__':
    game()
