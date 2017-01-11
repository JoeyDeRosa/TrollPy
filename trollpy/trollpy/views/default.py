from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models import User, KillScore, BoardPos
from ..security import check_credentials
import json

from PythonChess.ChessBoard import ChessBoard
from PythonChess.ChessAI import ChessAI_random
from PythonChess.ChessGUI_text import ChessGUI_text
from PythonChess.ChessRules import ChessRules

empty_board = [['bR', 'bT', 'bB', 'bQ', 'bK', 'bB', 'bT', 'bR'],
               ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
               ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
               ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
               ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
               ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
               ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
               ['wR', 'wT', 'wB', 'wQ', 'wK', 'wB', 'wT', 'wR']]

@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request, new_fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
    """Render a chessboard with the current FEN."""
    #
    #  TODO: the <fen='kwarg'> should be updated by the game to render the
    #        board with the BoardPos model.
    #
    fen = new_fen
    board = BoardPos(fen=fen)
    return {"board": board}


@view_config(route_name='registration', renderer='../templates/registration.jinja2')
def registration_view(request):
    if request.method == "POST" and request.POST:
        if request.POST["username"] and len(request.POST["username"].split()) > 1:
            new_name = request.POST["username"].split()
            new_name = '_'.join(new_name)
        else:
            new_name = request.POST["username"]
        new_user = User(
            username=new_name or request.POST["username"],
            password=request.POST["password"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"]
        )
        request.dbsession.add(new_user)
        auth_head = remember(request, new_name)
        return HTTPFound(request.route_url('profile', userid=new_name), headers=auth_head)
    return {}


@view_config(route_name='login', renderer='../templates/login.jinja2')
def login_view(request):
    if request.method == "POST" and request.POST:
        if request.POST["username"] and len(request.POST["username"].split()) > 1:
            new_name = request.POST["username"].split()
            new_name = '_'.join(new_name)
            request.POST["username"] = new_name
        if check_credentials(request):
            auth_head = remember(request, request.POST["username"])
            return HTTPFound(request.route_url('home'), headers=auth_head)
    return {}


@view_config(route_name='logout')
def logout_view(request):
    empty_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=empty_head)


@view_config(route_name='profile', renderer='../templates/profile.jinja2')
def profile_view(request):
    theuserid = request.matchdict['userid']
    the_user = request.dbsession.query(User).filter_by(username=theuserid).first()
    return {"user": the_user}


@view_config(route_name='add_smack', renderer='../templates/add_smack.jinja2')
def add_smack(request):
    if request.method == "POST" and request.POST:
        new_killscore = KillScore(
            killscore_id=request.POST['killscore_id'],
            statement=request.POST['statement']
        )
        request.dbsession.add(new_killscore)
        return HTTPFound(request.route_url('add_smack'))
    return {}


@view_config(route_name='api_smack', renderer='json')
def smack_json(request):
    smack_dict = request.dbsession.query(KillScore).all()
    output = [item.to_json() for item in smack_dict]
    return output


@view_config(route_name='api_user', renderer='json')
def user_board_json(request):
    theuserid = request.matchdict['userid']
    user = request.dbsession.query(User).filter_by(username=theuserid)
    json = user.first().to_json()
    if not user.first().winner == 'None':
        user.update({'board': str(empty_board)})
    return json


@view_config(route_name='make_move')
def make_move(request):
    if request.method == "POST" and request.POST:
        rule = ChessRules()
        user_move = ChessGUI_text()
        theuserid = request.matchdict['userid']
        move = json.loads(request.POST['move'])
        a1 = tuple(move[0])
        a2 = tuple(move[1])
        move = (a1, a2)
        user = request.dbsession.query(User).filter_by(username=theuserid)
        board = empty_board
        # import pdb; pdb.set_trace()
        if rule.IsCheckmate(board, 'white'):
            user.update({'winner': 'AI'})
        elif rule.IsCheckmate(board, 'black'):
            user.update({'winner': 'User'})
        else:
            if rule.IsInCheck(board, 'white'):
                user.update({'in_check': True})
            else:
                user.update({'in_check': False})
                if user_move.GetPlayerInput(board, 'white', move):
                    print('Valid Move')
                    chess_board = ChessBoard(0)
                    chess_board.squares = board
                    chess_board.MovePiece(move)
                    ai = ChessAI_random('Trump', 'black')
                    ai_move = ai.GetMove(board, 'black')
                    chess_board.MovePiece(ai_move)
                    print(chess_board.GetState())
                    return HTTPFound(request.route_url('home'))
