import os
import sys
import transaction

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
    )

trash_talk = [{"killscore_id": -1, "id": 1, "statement": "Hey"}, {"killscore_id": -4, "id": 2, "statement": "You are performing worse than DMX in Exit Wounds"}, {"killscore_id": 8, "id": 3, "statement": "I would help you out, but you're beyond hope at this point"}, {"killscore_id": -3, "id": 4, "statement": "Why would you do that? Now I'm going destroy you"}, {"killscore_id": -1, "id": 5, "statement": "There's no one that can match me. My style is impetuous, my defense is impregnable, and I'm just ferocious. I want your heart! I want to eat your children!"}, {"killscore_id": 2, "id": 6, "statement": "First we gonna rock, then we gonna roll, Lex gonna give it to ya, baby go baby go"}, {"killscore_id": 0, "id": 7, "statement": "Do you want to talk to me? Or what do you want to do with me? Watch my eating techniques here? How I gorge the chicken? How I eat like a barracuda?"}, {"killscore_id": -4, "id": 8, "statement": "Look what you done started Asked for it, you got it Had it, should have shot it Now you're dearly departed Get at me, dog; did I rip shit? With this one here, I flip shit"}, {"killscore_id": -5, "id": 9, "statement": "What was that look for When I walked in the door? Oh, you thought you was raw? Boom! Not anymore 'Cause now you on the floor"}, {"killscore_id": 6, "id": 10, "statement": "Keep rolling your eyes. Maybe you'll find a brain back there."}, {"killscore_id": -3, "id": 11, "statement": "If you even dream of beating me, you better wake up and apologize.'"}, {"killscore_id": -7, "id": 12, "statement": "If I had to describe your face, I would say it's somewhere between a Llama's ass and a sloth's brain"}, {"killscore_id": 4, "id": 13, "statement": "HEY LOSER! I HEARD YOU THINK YOU CAN BEAT ME. WRONG! SAD."}]
 

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
