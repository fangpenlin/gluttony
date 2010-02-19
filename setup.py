# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='Gluttony',
    version='0.2',
    description= "A tool for find dependencies relationships among Python projects on PyPi",
    author='Victor Lin',
    author_email='bornstub@gmail.com',
    keywords='dependency relationship',
    url='http://code.google.com/p/python-gluttony/',
    install_requires=["Pip>=0.6.3"],
    packages=['gluttony'],
    license='MIT',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts': ['gluttony = gluttony:main']},
)
