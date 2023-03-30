from setuptools import setup

setup(
    name='flask-my-extension',
    entry_points='''
        [flask.commands]
        my-command=mypackage.commands:cli
    ''',
)