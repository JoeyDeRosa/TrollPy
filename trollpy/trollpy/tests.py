"""Tests for TrollyPy App."""
import pytest
import transaction
import os
from .chess_game import users_game
from pyramid import testing
from .models.meta import Base
from .models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    User,
    KillScore
)


@pytest.fixture(scope="function")
def sqlengine(request):
    """Return sql engine."""
    config = testing.setUp(settings={
        'sqlalchemy.url': os.environ["DATABASE_URL"]
    })
    config.include(".models")
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    def teardown():
        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(engine)

    request.addfinalizer(teardown)
    return engine


@pytest.fixture(scope="function")
def new_session(sqlengine, request):
    """Return new session."""
    session_factory = get_session_factory(sqlengine)
    session = get_tm_session(session_factory, transaction.manager)

    def teardown():
        transaction.abort()

    request.addfinalizer(teardown)
    return session


@pytest.fixture
def dummy_request(new_session, method="GET"):
    """Instantiate a fake HTTP Request, complete with a database session."""
    request = testing.DummyRequest()
    request.method = method
    request.dbsession = new_session
    return request


@pytest.fixture
def testapp():
    """Create an instance of webtests TestApp for testing routes."""
    from webtest import TestApp
    from trollpy import main

    app = main({}, **{'sqlalchemy.url': os.environ["DATABASE_URL"]})
    testapp = TestApp(app)

    session_factory = app.registry["dbsession_factory"]
    engine = session_factory().bind
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    return testapp


@pytest.fixture
def fill_the_db(testapp):
    """Fill the database with some model instances."""
    session_factory = testapp.app.registry["dbsession_factory"]
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        user = User(username='amos',
                    password='password',
                    first_name='Amos',
                    last_name='Boldor',
                    email='amosboldor@gmail.com')
        kill_score = KillScore(killscore_id='-8',
                               statement='You live because I allowed it.')
        dbsession.add(kill_score)
        dbsession.add(user)

# ======== UNIT TESTS ==========


def test_registration_view(dummy_request):
    """Test that adding a user adds a new user to the database."""
    pass

# ======== FUNCTIONAL TESTS ===========


def test_home_page_pops_up(testapp):
    """Test that home page get sent correctly."""
    response = testapp.get('/', status=200)
    assert response.status_code == 200


def test_login_leads_to_home(testapp, fill_the_db):
    """Test that after logging in it sends you to the home route."""
    response = testapp.post('/login',
                            params={'username': 'amos',
                                    'password': 'password'}).follow()
    assert response.status_code == 200


def test_login_show_form(testapp):
    """Test that the login route shows form."""
    response = testapp.get('/login', status=200)
    assert response.status_code == 200
    assert response.html.find('form')


def test_registration_show_form(testapp):
    """Test that the registration route shows form."""
    response = testapp.get('/login', status=200)
    assert response.status_code == 200
    assert response.html.find('form')


def test_profile_route(testapp, fill_the_db):
    """Test that the profile route pops up with correct info."""
    response = testapp.get('/profile/amos', status=200)
    assert 'amosboldor@gmail.com' in response.html.find_all('li')[-1].text
    assert 'Amos Boldor' in response.html.find_all('li')[-2].text


def test_smack_api_route(testapp, fill_the_db):
    """Test smack_api to return kill_score json."""
    response = testapp.get('/smack_api', status=200)
    assert len(response.json) == 1


# ======== GAME TESTS ===========

def test_game():
    """Test for game function works."""
    fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    assert not fen == users_game(fen)



