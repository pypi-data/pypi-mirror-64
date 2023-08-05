Change log
==========

Release 0.3.2
-------------

:Date: 2020-03-21

* removed jsonpickle for saving projects (now explicit JSON conversion, resolves issue #1)
* bug fix (Qt-GUI): loading project with fewer constants than currently defined caused crash

Release 0.3.1
-------------

:Date: 2020-03-09

* bug fix (in jinja2 template): Plot failed, when y-min./max. and title label were defined

Release 0.3.0
-------------

:Date: 2020-03-08

* complete restructuring - base modules are now in simple_plotter.core
* bug fixes: crashes with logarithmic axes using kivy-frontend fixed
* documentation: User guide added

Release 0.2.2
-------------

:Date: 2020-02-27

* support for kivy-garden/graph based plotting library added (enables support for Android version of simple-plotter)

Release 0.2.1
-------------

:Date: 2019-11-02

* bug fix: loading of example project from older version failed

Release 0.2.0
-------------

:Date: 2019-11-02

* code parser added (limits allowed imports, calls, etc.)
* code generator now uses jinja templates
* unit tests added
* export csv removed

Release 0.1.2
-------------

:Date: 2019-10-18

* automatic version strings added (using setuptools_scm)
* package definitions moved from meta.yaml to setup.py

Release 0.1.1
-------------

:Date: 2019-10-14

* fixed documentation builds

Release 0.1.0
-------------

:Date: 2019-10-14

* Initial release