from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models import User, KillScore, Audio
from ..security import check_credentials
from pyramid.response import Response

from passlib.apps import custom_app_context as pwd_context

from ..chess_game import users_game
from gtts import gTTS
import os


@view_config(route_name='home', renderer='../templates/home.jinja2', require_csrf=False)
def home_view(request):
    """Render a chessboard with the current FEN."""
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
        fen = user.board
    else:
        fen = '8/8/8/8/8/8/8/8'
        user = None
    return {"py_board": fen, "user": user}


@view_config(route_name='registration', renderer='../templates/registration.jinja2', require_csrf=False)
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
            email=request.POST["email"],
            admin=False
        )
        request.dbsession.add(new_user)
        auth_head = remember(request, new_name)
        return HTTPFound(request.route_url('profile', userid=new_name), headers=auth_head)
    if request.authenticated_userid:
        return HTTPFound(request.route_url('profile', userid=request.authenticated_userid))
    else:
        user = None
    return {"user": user}


@view_config(route_name='login', renderer='../templates/login.jinja2', permission='view', require_csrf=False)
def login_view(request):
    if request.method == "POST" and request.POST:
        if request.POST["username"] and len(request.POST["username"].split()) > 1:
            new_name = request.POST["username"].split()
            new_name = '_'.join(new_name)
            request.POST["username"] = new_name
        if check_credentials(request):
            auth_head = remember(request, request.POST["username"])
            return HTTPFound(request.route_url('home'), headers=auth_head)
    if request.authenticated_userid:
        return HTTPFound(request.route_url('profile', userid=request.authenticated_userid))
    else:
        user = None
    return {"user": user}


@view_config(route_name='logout', require_csrf=False)
def logout_view(request):
    empty_head = forget(request)
    return HTTPFound(request.route_url('home'), headers=empty_head)


@view_config(route_name='profile', renderer='../templates/profile.jinja2', permission="view", require_csrf=True)
def profile_view(request):
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    theuserid = request.matchdict['userid']
    profile = request.dbsession.query(User).filter_by(username=theuserid).first()
    if request.method == 'POST' and request.POST:
        if request.POST["password"] != '':
            profile.password = pwd_context.hash(request.POST["password"])
        if profile.first_name != '':
            profile.first_name = request.POST["first_name"]
        if profile.last_name != '':
            profile.last_name = request.POST["last_name"]
        if profile.email != '':
            profile.email = request.POST["email"]
        return HTTPFound(request.route_url('profile', userid=theuserid))
    return {"profile": profile, "user": user}


@view_config(route_name='add_smack', renderer='../templates/add_smack.jinja2', permission="add", require_csrf=True)
def add_smack(request):
    """Add smack talk to the DB."""
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    if request.method == "POST" and request.POST:
        new_killscore = KillScore(
            killscore_id=request.POST['killscore_id'],
            statement=request.POST['statement']
        )
        request.dbsession.add(new_killscore)
        mp3_id = request.dbsession.query(KillScore).filter_by(statement=request.POST['statement']).first().id
        tts = gTTS(text=request.POST['statement'], lang='en')
        tts.save("hello.mp3")
        current_place = os.path.dirname(os.path.abspath(__file__))[:-13] + 'hello.mp3'
        print(current_place)
        with open(current_place, 'rb') as a:
            data = a.read()
        mp3 = Audio(id=mp3_id, binary_file=data)
        request.dbsession.add(mp3)
        print('mp3 id: ', mp3_id)
        return HTTPFound(request.route_url('add_smack'))
    killscore = request.dbsession.query(KillScore).all()
    return {"user": user, "killscore": killscore}


@view_config(route_name='del_smack', permission="view", require_csrf=False)
def del_smack(request):
    smack_id = request.matchdict['id']
    item_to_delete = request.dbsession.query(KillScore).get(smack_id)
    mp3_to_delete = request.dbsession.query(Audio).get(smack_id)
    request.dbsession.delete(item_to_delete)
    print('\nID ', smack_id)
    request.dbsession.delete(mp3_to_delete)
    return HTTPFound(request.route_url('add_smack'))


@view_config(route_name='api_smack', renderer='json', permission="view", require_csrf=False)
def smack_json(request):
    smack_dict = request.dbsession.query(KillScore).all()
    output = [item.to_json() for item in smack_dict]
    return output


@view_config(route_name='api_user', renderer='json', permission="view",require_csrf=False)
def user_board_json(request):
    theuserid = request.matchdict['userid']
    user = request.dbsession.query(User).filter_by(username=theuserid)
    stuff = user.first().to_json()
    # import pdb; pdb.set_trace()
    mp3_id = request.dbsession.query(KillScore).filter_by(statement=user.first().to_json()['trollspeak']).first().id
    stuff['id'] = mp3_id
    return stuff


@view_config(route_name='make_move', permission="view", require_csrf=False)
def make_move(request):
    if request.method == "POST" and request.POST:
        theuserid = request.matchdict['userid']
        board = request.POST['board']
        user = request.dbsession.query(User).filter_by(username=theuserid)
        board_winner = users_game(board, request, theuserid)
        if not board_winner[1]:
            user.update({'winner': board_winner[1], 'board': board_winner[0]})
        user.update({'board': board_winner[0]})
        return HTTPFound(request.route_url('home'))


@view_config(route_name='mp3')
def send_mp3(request):
    mp3_id = request.matchdict['id']
    data = request.dbsession.query(Audio).filter_by(id=mp3_id).first().binary_file
    return Response(content_type='audio/mpeg', body=data)

  
@view_config(route_name='userlist',
             permission="add",
             renderer='../templates/userlist.jinja2',
             require_csrf=True)
def user_list(request):
    """Return a list of all users in the DB."""
    if request.authenticated_userid:
        user = request.dbsession.query(User).filter_by(
            username=request.authenticated_userid).first()
    else:
        user = None
    users = request.dbsession.query(User).all()
    return {"users": users, "user": user}


@view_config(route_name='del_user', permission="view", require_csrf=False)
def del_user(request):
    user_id = request.matchdict['userid']
    item_to_delete = request.dbsession.query(User).get(user_id)
    request.dbsession.delete(item_to_delete)
    return HTTPFound(request.route_url('userlist'))

