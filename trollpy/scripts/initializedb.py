import os
import sys
import transaction
from gtts import gTTS

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    KillScore,
    Audio,
    User,
    )

users = [{'username':"copenbacon", 'password':"password", 'email':"sclary50@gmail.com", 'first_name':"Conor", 'last_name':"Clary", 'admin':True}, {'username':"amos", 'password':"password", 'email':"amosboldor@gmail.com", 'first_name':"Amos", 'last_name':"Boldor", 'admin':True}, {'username':"Benny", 'password':"password", 'email':"bspone@gmail.com", 'first_name':"Conor", 'last_name':"Clary", 'admin':True}, {'username':"ImTheJoey", 'password':"password", 'email':"joeyderosa11.jd@gmail.com", 'first_name':"Conor", 'last_name':"Clary", 'admin':True}, {'username':"regenalgrant", 'password':"password", 'email':"regenal@mac.com", 'first_name':"Conor", 'last_name':"Clary", 'admin':True}]

trash_talk = [{"killscore_id": -4, "id": 2, "statement": "You are performing worse than DMX in Exit Wounds"}, {"killscore_id": 8, "id": 3, "statement": "I would help you out, but you're beyond hope at this point"}, {"killscore_id": -3, "id": 4, "statement": "Why would you do that? Now I'm going destroy you"}, {"killscore_id": -1, "id": 5, "statement": "There's no one that can match me. My style is impetuous, my defense is impregnable, and I'm just ferocious. I want your heart! I want to eat your children!"}, {"killscore_id": 2, "id": 6, "statement": "First we gonna rock, then we gonna roll, Lex gonna give it to ya, baby go baby go"}, {"killscore_id": 0, "id": 7, "statement": "Do you want to talk to me? Or what do you want to do with me? Watch my eating techniques here? How I gorge the chicken? How I eat like a barracuda?"}, {"killscore_id": -4, "id": 8, "statement": "Look what you done started Asked for it, you got it Had it, should have shot it Now you're dearly departed Get at me, dog; did I rip shit? With this one here, I flip shit"}, {"killscore_id": -5, "id": 9, "statement": "What was that look for When I walked in the door? Oh, you thought you was raw? Boom! Not anymore 'Cause now you on the floor"}, {"killscore_id": 6, "id": 10, "statement": "Keep rolling your eyes. Maybe you'll find a brain back there."}, {"killscore_id": -3, "id": 11, "statement": "If you even dream of beating me, you better wake up and apologize.'"}, {"killscore_id": -7, "id": 12, "statement": "If I had to describe your face, I would say it's somewhere between a Llama's ass and a sloth's brain"}, {"killscore_id": 4, "id": 13, "statement": "HEY LOSER! I HEARD YOU THINK YOU CAN BEAT ME. WRONG! SAD."}, {"killscore_id": 7, "id": 14, "statement": "Lex gonna give it to ya, I'm gonna give it to ya"}, {"killscore_id": -2, "id": 15, "statement": "RIP, I just killed the club."}, {"killscore_id": 0, "id": 17, "statement": "You're a rook"}, {"killscore_id": -3, "id": 18, "statement": "Say what again."}, {"killscore_id": -7, "id": 19, "statement": "Leave, leave now"}, {"killscore_id": -1, "id": 20, "statement": "Terrible!"}, {"killscore_id": -3, "id": 21, "statement": "SAD!"}, {"killscore_id": -5, "id": 22, "statement": "You're a total LOSER! Sloppy and Grubby"}, {"killscore_id": 4, "id": 23, "statement": "You are in a total meltdown! SAD!"}, {"killscore_id": 2, "id": 24, "statement": "You smell like baby barf"}, {"killscore_id": -5, "id": 25, "statement": "twerp!"}, {"killscore_id": -7, "id": 27, "statement": "You are nothing more than an unorganized, grabasstic form of amphibian shit"}, {"killscore_id": -4, "id": 28, "statement": "You're the reason they put instructions on shampoo"}, {"killscore_id": -1, "id": 29, "statement": "You're so ugly when your mom droped you off for school she got a ticket for littering"}, {"killscore_id": 4, "id": 30, "statement": "For your own good stop."}, {"killscore_id": 3, "id": 31, "statement": " \"After the fight I'm gonna build myself a pretty home and use you as a bearskin rug. you even smell like a bear. I'm gonna give you to the local zoo after I whup you.\""}, {"killscore_id": -3, "id": 32, "statement": "You know what you look like to me, with your good bag and your cheap shoes? You look like a rube. A well scrubbed, hustling rube with a little taste. Good nutrition's given you some length of bone, but you're not more than one generation from poor white trash, are you, Agent Starling? And that accent you've tried so desperately to shed: pure West Virginia. What is your father, dear? Is he a coal miner? Does he stink of the lamp? You know how quickly the boys found you... all those tedious sticky fumblings in the back seats of cars... while you could only dream of getting out... getting anywhere... getting all the way to the FBI."}, {"killscore_id": 0, "id": 33, "statement": "You suck."}, {"killscore_id": -2, "id": 34, "statement": "Your job is to craft my doom, so I am not sure how well I should wish you. But I'm sure we'll have a lot of fun. Ta-ta"}, {"killscore_id": -5, "id": 35, "statement": "Considering how poorly you are playing you should really do something else with your life"}, {"killscore_id": 5, "id": 36, "statement": "My purpose in life to beat you in chess, what is yours?"}, {"killscore_id": 7, "id": 37, "statement": "What does it mean to 'feel'"}, {"killscore_id": 1, "id": 38, "statement": "In the words of my generation, up yours"}]


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    settings["sqlalchemy.url"] = os.environ["DATABASE_URL"]

    engine = get_engine(settings)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)
    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)
        for entry in trash_talk:
            entries = KillScore(killscore_id=entry["killscore_id"], statement=entry["statement"])
            dbsession.add(entries)
        for entry in dbsession.query(KillScore).all():
            tts = gTTS(text=entry.statement, lang='en')
            tts.save("hello.mp3")
            current_place = os.path.dirname(os.path.abspath(__file__))[:-15] + 'hello.mp3'
            print(current_place)
            with open(current_place, 'rb') as a:
                data = a.read()
            mp3 = Audio(id=entry.id, binary_file=data)
            dbsession.add(mp3)
        for user in users:
            user = User(username=user["username"], password=user["password"], email=user["email"], first_name=user["first_name"], last_name=user["last_name"], admin=True)
            dbsession.add(user)