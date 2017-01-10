from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget
from ..models import User
from ..security import check_credentials



@view_config(route_name='home', renderer='../templates/home.jinja2')
def home_view(request):
    # import pdb; pdb.set_trace()
    return {}


@view_config(route_name='registration', renderer='../templates/registration.jinja2')
def registration_view(request):
    if request.method == "POST" and request.POST:
        if request.POST["username"] and len(request.POST["username"].split()) > 1:
            new_name = request.POST["username"].split()
            new_name = '_'.join(new_name)
        new_user = User(
            username=new_name,
            password=request.POST["password"],
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            email=request.POST["email"]
        )
        request.dbsession.add(new_user)
        return HTTPFound(request.route_url('home'))
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
    # import pdb; pdb.set_trace()
    return {"user": the_user}
