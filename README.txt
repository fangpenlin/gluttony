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
For understanding optons of Gluttony, you can type:
::

    gluttony --help
    
Also, once your're familiar with pip install, most of the options are same.

Drawing Graph
=============

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

.. image:: http://static.ez2learn.com/gluttony/tg2.png

Oops, the graph is a mess.  I didn't handle layout of graph.  I have not time 
to finish it right now.  Fortunately, you can output the graph as dot or 
pickle format file for further handling.

Output Graphviz File
====================
In order to draw the diagram with Graphviz, you can output that format.
For example:

::

    gluttony sprox --pydot sprox.dot
	
Then you can use `Graphviz <http://www.graphviz.org/>`_ for drawing beautiful 
graph. Like this one:

.. image:: http://static.ez2learn.com/gluttony/sprox_dot.png

Another huge example:

`Dependency relationship digram of TurboGears2 <http://static.ez2learn.com/gluttony/tg2_dot.png>`_

Output Pickle File
==================
If you want to get the relationships data in Python form, this tool also 
provide a pickle output. For example:

::

    gluttony sprox --pickle sprox.pickle
	
Then you can use pickle.load for further processing.

Gallery
=======

`Gallery <http://code.google.com/p/python-gluttony/wiki/Gallery>`_

Author
======

 * Victor Lin (bornstub at gmail.com)
 * Twitter: `victorlin <http://twitter.com/victorlin>`_
 * Blog: `Victor's Blog <http://blog.ez2learn.com>`_