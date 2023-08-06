try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config = {
    'description': 'this be a simplez testeroozz',
    'author': 'ilja',
    'author_email': 'testeroozz@gmail.com',
    'version': '0.8',
    'long_description': 'coronaviruzzzzed',
    'install_requires': ['nose'],
    'packages': ['testeroozz'],
    'scripts': ['bin/script1'],
    'name': 'testeroozz'
}

setup(**config)
