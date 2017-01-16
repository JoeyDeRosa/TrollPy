"""Setup."""


import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'ipython',
    'pyramid_ipython',
    'psycopg2',
    'passlib',
    'python-chess',
    'gTTS',
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest',  # includes virtualenv
    'pytest-cov',
    'tox',
]

setup(name='trollpy',
      version='0.0',
      description='trollpy app for chess with alexa',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='Amos Boldor,Conor Clary, Joey Derosa, Regenal Grant, Benjamin Petty',
      author_email='conor.clary@gmail.com, regenal@mac.com, amosboldor@gmail.com, joeyderosa11.jd@gmail.com, Benjamin.s.petty@gmail.com,',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      package_dir={'': '.'},
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'testing': tests_require,
      },
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = trollpy:main
      [console_scripts]
      initialize_db = trollpy.scripts.initializedb:main
      """,
      )
