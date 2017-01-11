import unittest
import transaction

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMyViewSuccessCondition(BaseTest):

    def setUp(self):
        super(TestMyViewSuccessCondition, self).setUp()
        self.init_database()

        from .models import MyModel

        model = MyModel(name='one', value=55)
        self.session.add(model)

    def test_passing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info['one'].name, 'one')
        self.assertEqual(info['project'], 'trollpy')


class TestMyViewFailureCondition(BaseTest):

    def test_failing_view(self):
        from .views.default import my_view
        info = my_view(dummy_request(self.session))
        self.assertEqual(info.status_int, 500)


def test_chess_ai():
    """Test that chess ai is creted."""
    from ..PythonChess.ChessAI import ChessAI
    bot = ChessAI('troll', 'white')
    assert bot.GetName() is 'troll' and bot.GetColor() is 'white'


def test_chess_ai_random_get_move():
    """Test for the get move method of the chess ai random class."""
    from ..PythonChess.ChessAI import ChessAI_random
    bot = ChessAI_random


# @pytest.fixture
# def testapp():
#     """Test an instance of webtests TestApp for testing routes."""
#
#     from webtest import TestApp
#     from mymodel import main
#
#     app = main({}, **{"sqlalchemy.url": 'sqlite:///:memory:'})
#     testapp = TestApp(app)
#
#     SessionFactory = app.registry["dbsession_factory"]
#     engine = SessionFactory().bind
#     Base.metadata.create_all(bind=engine)
#
#     return testapp
#
#
# @pytest.fixture
# def set_auth_credentials():
#     """Make a username/password combo for testing."""
#     import os
#     from passlib.apps import custom_app_context as pwd_context
#
#     os.environ["AUTH_USERNAME"] = "testme"
#     os.environ["AUTH_PASSWORD"] = pwd_context.hash("foobar")
#
#
# @pytest.fixture
# def fill_the_db(testapp):
#     """Fill the database with some model instances.
#     Start a database session with the transaction manager and add all of the
#     expenses. This will be done anew for every test.
#     """
#     SessionFactory = testapp.app.registry["dbsession_factory"]
#     with transaction.manager:
#         dbsession = get_tm_session(SessionFactory, transaction.manager)
#         dbsession.add_all()
#
#
# def test_home_route_has_table(testapp):
#     """The home page has a table in the html."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(html.find_all("table")) == 1
#
#
# def test_home_route_with_data(testapp, fill_the_db):
#     """When there's data in the database, the home page has some rows."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(html.find_all("tr")) == 101
#
#
# def test_home_route(testapp):
#     """Without data the home page only has the header row in its table."""
#     response = testapp.get('/', status=200)
#     html = response.html
#     assert len(html.find_all("tr")) == 1
