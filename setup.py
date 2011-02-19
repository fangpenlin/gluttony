# -*- coding: utf-8 -*-
from distribute_setup import use_setuptools
use_setuptools()
    
from setuptools import setup
    
extra = {}
try:
    extra['long_description']=open('README.rst').read(),
except IOError:
    pass

try:
    import gluttony
    extra['version'] = gluttony.__version__
except ImportError:
    pass

setup(
    name='Gluttony',
    description= "A tool for find dependencies relationships among Python "
                 "projects on PyPi",
    author='Victor Lin',
    author_email='bornstub@gmail.com',
    keywords='package dependency relationship',
    url='http://bitbucket.org/victorlin/gluttony',
    install_requires=[
        "Pip>=0.8", 
        "networkx>=1.0.1"
    ],
    packages=['gluttony'],
    license='MIT',
    entry_points={
        'console_scripts': ['gluttony = gluttony.gluttony:main']
    }, **extra
)
