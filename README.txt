========
Gluttony
========

Gluttony is a tool for finding dependency relationships among Python 
prjects in PyPi, it is based on `pip <http://pip.openplans.org/>`_.

.. image:: http://static.ez2learn.com/gluttony/gluttony.jpg

Installation
============

To install Gluttony

::

    easy_install Gluttony

Usage
=====

To know dependency relationships

::

    gluttony <project name> --display-graph

For example: you want to know the dependency relationships of a 
Python project `Sprox <http://sprox.org/>`_, then you can type::

    gluttony sprox --display-graph

The result might looks like this:

.. image:: http://static.ez2learn.com/gluttony/sprox.png

Also, it also supports most of command of ``pip install``, for example: 
you want to know the relations among `TurboGears2 <http://turbogears.org/>`_ packages, here we type

::

    gluttony -i http://www.turbogears.org/2.0/downloads/current/index tg.devtools --display-graph

The result:

.. image:: http://static.ez2learn.com/gluttony/turbogears2.jpg

Oops, the graph is a mess.  I didn't handle layout of graph.  
I have not time to finish it right now.  Fortunately, if you want to get the 
relationships data in Python form, this tool also provide a pickle output. 
For example:

::

    gluttony sprox --pickle sprox.pickle
	
Then you can use pickle.load for further processing.

Author
======

 * Victor Lin (bornstub at gmail.com)
 * Twitter: `victorlin <http://twitter.com/victorlin>`_
 * Blog: `Victor's Blog <http://blog.ez2learn.com>`_