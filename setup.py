# -*- coding-: utf-8 -*-
from setuptools import setup

setup(
    name='http-server',
    description='http-server for SEA PY 401d4',
    version=0.1,
    author='Jeff Torres, Tatiana Weaver',
    author_email='email@email.com',
    license='MIT',
    py_modules=['client, server'],
    package_dir={'': 'src'},
    install_requires=[],
    extras_require={'test': ['pytest', 'tox']},
    entry_points={}
)
