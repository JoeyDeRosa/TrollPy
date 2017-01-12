"""Chess game."""


import chess
import random
from .models import KillScore, User


def users_game(user_board, request, theuserid):
    """The game for the specific user."""
    winner = None

    def game(user_board):
        """Run the chess game."""
        board = get_board(user_board)
        print(board)
        board.set_fen(user_board)
        if board.is_game_over():
            winner = 'User'
        print(board)
        print(board.fen())
        troll_move = troll(board)
        talk_shit(troll_move, board)
        board.push(troll_move)
        if board.is_game_over():
            winner = 'Troll'
        return board.fen()

    def get_board(user_board):
        """Get the board setup that will be used."""
        board = chess.Board(user_board)
        return board

    def troll(board):
        """Generate a move for the troll."""
        moves = {
            'prioritize_king_one': [],
            'prioritize_king_two': [],
            'high_priority_moves': [],
            'med_priority_moves': [],
            'low_priority_moves': [],
        }
        moves = prioritize_troll_moves(moves, board)
        prefered_move_list = select_move_list(moves, board)
        troll_move = random.randint(0, len(prefered_move_list) - 1)
        return prefered_move_list[troll_move]

    def prioritize_troll_moves(moves, board):
        """Return a dictionary of the trolls moves seperated by priority."""
        for move in board.legal_moves:
            if board.is_capture(move):
                if board.is_attacked_by(chess.WHITE, move.to_square):
                    moves['med_priority_moves'].append(move)
                else:
                    board.push(move)
                    if board.is_check():
                        board.pop()
                        moves['prioritize_king_one'].append(move)
                    else:
                        board.pop()
                        moves['high_priority_moves'].append(move)
            else:
                if board.is_attacked_by(chess.WHITE, move.to_square):
                    moves['low_priority_moves'].append(move)
                else:
                    board.push(move)
                    if board.is_check():
                        board.pop()
                        moves['prioritize_king_two'].append(move)
                    else:
                        board.pop()
                        moves['med_priority_moves'].append(move)
        return moves

    def select_move_list(moves, board):
        """Return the list of moves with the highest priority for the troll to choose from."""
        if len(moves['prioritize_king_one']) > 0:
            return moves['prioritize_king_one']
        if len(moves['prioritize_king_two']) > 0:
            return moves['prioritize_king_two']
        if len(moves['high_priority_moves']) > 0:
            return moves['high_priority_moves']
        if len(moves['med_priority_moves']) > 0:
            return moves['med_priority_moves']
        return moves['low_priority_moves']

    def talk_shit(troll_move, board):
        piece_lvl = {
            'K': 9,
            'Q': 8,
            'B': 4,
            'N': 3,
            'R': 2,
            'P': 1,
        }
        if board.piece_at(troll_move.to_square) is None:
            print('Baaaadum Baaadum Badum BadumBaduBadem.')
        else:
            print(board.piece_at(troll_move.to_square), " :piece at")
            # import pdb; pdb.set_trace()

            piece_taken = str(board.piece_at(troll_move.to_square).symbol()).upper()
            piece_moved = str(board.piece_at(troll_move.from_square).symbol()).upper()
            print(piece_taken, piece_moved)

            lvl = piece_lvl[piece_taken] - piece_lvl[piece_moved]
            print(lvl)
            shit_talk = request.dbsession.query(KillScore).filter_by(killscore_id=lvl).all()
            if shit_talk:
                print(random.choice(shit_talk).statement)
                user = request.dbsession.query(User).filter_by(username=theuserid)
                user.update({'trollspeak': random.choice(shit_talk).statement})
    troll_move = game(user_board)
    return (troll_move, winner)
