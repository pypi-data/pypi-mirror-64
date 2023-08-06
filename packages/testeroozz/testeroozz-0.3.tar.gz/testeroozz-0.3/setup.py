try:
    from setuptools import setup
except ImportError:
    from disutils.core import setup

config = {
    'description': 'this be a simplez testeroozz',
    'author': 'ilja',
    'author_email': 'testeroozz@gmail.com',
    'version': '0.3',
    'install_requires': ['nose'],
    'packages': ['testeroozz'],
    'scripts': [],
    'name': 'testeroozz'
}

setup(**config)
