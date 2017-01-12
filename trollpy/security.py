# security.py
import os
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from trollpy.models import User
from passlib.apps import  custom_app_context as pwd_context

def check_credentials(request):
    if "username" in request.POST and "password" in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        query = request.dbsession.query(User)
        the_user = query.filter(User.username == username).first()
        if the_user:
            if pwd_context.verify(password, the_user.password):
                return True

    return False

def includeme(config):
    """security-related configuration"""
    auth_secret = os.environ.get('AUTH_SECRET', 'itsaseekrit')
    authn_policy = AuthTktAuthenticationPolicy(
        secret=auth_secret,
        hashalg='sha512'
    )
    config.set_authentication_policy(authn_policy)
    authz_policy = ACLAuthorizationPolicy()
    config.set_authorization_policy(authz_policy)