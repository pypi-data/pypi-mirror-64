.. simple_plotter documentation master file, created by
   sphinx-quickstart on Sun Oct 13 17:18:15 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to simple_plotter's documentation!
==========================================

*simple-plotter* is a code-generator to create python code for plotting functional 2D x,y-plots.
The function equation has to be entered in python syntax (allowing the use of numpy statements).

*simple-plotter* provides a command line interface (CLI) tool, which takes simple JSON files as inputs to generate the
code.

Graphical user interface (GUI) front-ends for *simple-plotter* are available as well.

The `simple-plotter-qt`_ package provides with a Qt-based GUI-frontend intended for desktop use.

simple-plotter4a_ provides an alternative kivy-based frontend, created primarily for the Android port (see screen shots
below), which can be used on a desktop system as well.

For details on licenses see :ref:`licenses` or the NOTICE and LICENSE files in the source code repositories of the
individual components.

.. figure:: screen_shot_qt.png

   Screen shot of the Qt-based GUI

.. figure:: screen_shot_android.png

   Screen shot of the kivy-based GUI (running on Android)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   howto.rst
   user_guide.rst
   license.rst
   dev_guide.rst
   api.rst
   roadmap.rst
   changelog.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _simple-plotter4a: https://gitlab.com/thecker/simple-plotter4a
.. _simple-plotter-qt: https://gitlab.com/thecker/simple-plotter-qt
