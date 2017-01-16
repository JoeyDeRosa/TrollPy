"""Routes."""


def includeme(config):
    """Include these routes."""
    config.add_static_view(name='static', path='static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('registration', '/registration')
    config.add_route('profile', '/profile/{userid:[\d\w]+}')
    config.add_route('add_smack', '/add_smack')
    config.add_route('api_smack', '/smack_api')
    config.add_route('api_user', '/{userid:[\d\w]+}/api')
    config.add_route('make_move', '/{userid:[\d\w]+}/move')
    config.add_route('mp3', '/mp3/{id:\d+}')
    config.add_route('del_smack', '/delete/{id:[\d]+}')
    config.add_route('userlist', '/userlist')
    config.add_route('del_user', '/delete_user/{userid:[\d\w]+}')
