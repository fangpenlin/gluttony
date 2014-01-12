# -*- coding: utf-8 -*-
import os
from distribute_setup import use_setuptools
use_setuptools()
    
from setuptools import setup
    
here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.txt')).read()
requires = open(os.path.join(here, 'requirements.txt')).read()
requires = map(lambda r: r.strip(), requires.splitlines())
test_requires = open(os.path.join(here, 'test-requirements.txt')).read()
test_requires = map(lambda r: r.strip(), test_requires.splitlines())

extra = {}
try:
    import gluttony
    extra['version'] = gluttony.__version__
except ImportError:
    pass

setup(
    name='Gluttony',
    description="A tool for find dependencies relationships between Python "
                "packages",
    author='Victor Lin',
    author_email='bornstub@gmail.com',
    keywords='package dependency relationship',
    long_description=readme,
    url='http://github.com/victorlin/gluttony',
    install_requires=requires,
    tests_require=test_requires,
    include_package_data=True,
    packages=['gluttony'],
    license='MIT',
    entry_points={
        'console_scripts': ['gluttony = gluttony.commands:main']
    }, 
    **extra
)
