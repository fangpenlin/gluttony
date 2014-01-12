Gluttony
--------

|Build Status|

Gluttony is a tool for finding dependencies relationship of a Python
package.

.. figure:: http://static.ez2learn.com/gluttony/gluttony.jpg
   :alt: Gluttony

Installation
------------

To install Gluttony

::

    pip install Gluttony

Usage
-----

To understand the available optons of Gluttony, you can type:

::

    gluttony --help

Drawing Graph
-------------

To figure out the dependencies relationship of a Python package, here
you can type (the diagram will be displayed by
`matplotlib <http://matplotlib.org/>`__, you need to install it before
you can use --display-graph option)

::

    gluttony <package name> --display-graph

For example, you would like to know the dependency relationships of
`Sprox <http://sprox.org/>`__, then you can type:

::

    gluttony sprox --display-graph

The result might looks like this:

.. figure:: http://static.ez2learn.com/gluttony/sprox.png
   :alt: Sproxy dependencies diagram

Another example example: you want to understand the dependencies
relationship of `TurboGears2 <http://turbogears.org/>`__, here we type

::

    gluttony -i http://www.turbogears.org/2.0/downloads/current/index tg.devtools --display-graph

The result:

.. figure:: http://static.ez2learn.com/gluttony/tg2.png
   :alt: Turbogears2 dependencies diagram

Oops, the graph is a little bit messy. Currently, the layout of graph is
not handled properly. However, it's not a big deal, you can output the
graph as dot or pickle format file for further processing.

Output Graphviz File
--------------------

To draw the diagram with Graphviz, you can output that dot format like
this

::

    gluttony sprox --pydot sprox.dot

Then you can use `Graphviz <http://www.graphviz.org/>`__ for drawing
beautiful graph. Like this one:

.. figure:: http://static.ez2learn.com/gluttony/sprox_dot.png
   :alt: Sproxy dependencies diagram

Another huge example:

.. figure:: http://static.ez2learn.com/gluttony/tg2_dot.png
   :alt: Dependency relationship digram of TurboGears2

Output Pickle File
------------------

If you want to get the raw relationship data in Python, this tool also
provides a pickle output format. For example:

::

    gluttony sprox --pickle sprox.pickle

Then you can use ``pickle.load`` to load it into Python for further
processing.

Gallery
-------

See some beautiful Python package dependencies relationship diagram :)

`Gallery <http://code.google.com/p/python-gluttony/wiki/Gallery>`__

Author
------

-  Victor Lin (bornstub at gmail.com)
-  Twitter: `victorlin <http://twitter.com/victorlin>`__
-  Blog: `Victor's Blog <http://victorlin.me>`__

.. |Build Status| image:: https://travis-ci.org/victorlin/gluttony.png?branch=master
   :target: https://travis-ci.org/victorlin/gluttony
