# TrollPy
TrollPy is an interactive bot that will deliver the appropriate ammount of trash talk relative to how well or poorly you are performing in a game of chess against it.

### Tools:
- Python-Chess
- Chess.js
- Chessboard.js
- gTTS
- Pyramid
- Zurb Foundation
- Postgres

### Creators:
- Joey DeRosa (https://github.com/JoeyDeRosa)
- Ben Petty (https://github.com/benpetty)
- Regenal Grant (https://github.com/regenalgrant)
- Amos Boldor (https://github.com/amosboldor)
- Conor Clary (https://github.com/Copenbacon)

### Testing
```
- coverage: platform darwin, python 2.7.12-final-0 ---
Name                              Stmts   Miss  Cover
------------------------------------------------------
trollpy/__init__.py                  11      0   100%
trollpy/chess_game.py               126     58    54%
trollpy/models/__init__.py           22      0   100%
trollpy/models/meta.py                5      0   100%
trollpy/models/mymodel.py            43      0   100%
trollpy/routes.py                    15      0   100%
trollpy/scripts/__init__.py           0      0   100%
trollpy/scripts/initializedb.py      43     31    28%
trollpy/security.py                  33      0   100%
trollpy/tests.py                    175     25    86%
trollpy/views/__init__.py             0      0   100%
trollpy/views/default.py            128      7    95%
trollpy/views/notfound.py             4      2    50%
------------------------------------------------------
TOTAL                               605    123    80%

-- coverage: platform darwin, python 3.5.2-final-0 ---
Name                              Stmts   Miss  Cover
------------------------------------------------------
trollpy/__init__.py                  11      0   100%
trollpy/chess_game.py               126     58    54%
trollpy/models/__init__.py           22      0   100%
trollpy/models/meta.py                5      0   100%
trollpy/models/mymodel.py            43      0   100%
trollpy/routes.py                    15      0   100%
trollpy/scripts/__init__.py           0      0   100%
trollpy/scripts/initializedb.py      43     31    28%
trollpy/security.py                  33      0   100%
trollpy/tests.py                    175     25    86%
trollpy/views/__init__.py             0      0   100%
trollpy/views/default.py            128      7    95%
trollpy/views/notfound.py             4      2    50%
------------------------------------------------------
TOTAL                               605    123    80%
```

