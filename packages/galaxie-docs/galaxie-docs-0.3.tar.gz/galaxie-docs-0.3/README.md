[![pipeline status](https://gitlab.com/Tuuux/galaxie-docs/badges/master/pipeline.svg)](https://gitlab.com/Tuuux/galaxie-docs/-/commits/master) [![coverage report](https://gitlab.com/Tuuux/galaxie-docs/badges/master/coverage.svg)](https://gitlab.com/Tuuux/galaxie-docs/-/commits/master) [![Documentation Status](https://readthedocs.org/projects/galaxie-docs/badge/?version=latest)](https://galaxie-docs.readthedocs.io/en/latest/?badge=latest)

Galaxie Docs, The ToolKit
===========================
<div style="text-align:center"><img src ="https://gitlab.com/Tuuux/galaxie-curses/raw/master/docs/source/images/logo_galaxie.png" /></div>

The Project
-----------
**Galaxie Docs** is a free software Tool Kit for create MarkDown to HTML file.

Then the lib is write in **Python**

Installation
------------

**Pre Version**: ```pip install galaxie-docs```<BR>
**Dev Version**: ```pip install -i https://test.pypi.org/simple/ galaxie-docs```

Documentation:
-------------
* **Readthedocs link:** http://galaxie-docs.readthedocs.io
* **Packages documentation:** https://galaxie-docs.readthedocs.io/en/latest/GLXDocs.html

The Mission
-----------
Galaxie have choose Markdown format as text format, then the lib have target to convert documents around MarkDown.

Contribute
----------
You welcome !!!

- Issue Tracker: https://gitlab.com/Tuuux/galaxie-docs/issues
- Source Code: https://gitlab.com/Tuuux/galaxie-docs

Screenshots
-----------

**The source**
```markdown
[![Documentation Status](https://readthedocs.org/projects/galaxie-curses/badge/?version=latest)](http://galaxie-curses.readthedocs.io/?badge=latest)
[![pipeline status](https://gitlab.com/Tuuux/galaxie-curses/badges/master/pipeline.svg)](https://gitlab.com/Tuuux/galaxie-curses/-/commits/master)
[![coverage report](https://gitlab.com/Tuuux/galaxie-curses/badges/master/coverage.svg)](https://gitlab.com/Tuuux/galaxie-curses/-/commits/master)
[![codecov](https://codecov.io/gl/Tuuux/galaxie-curses/branch/master/graph/badge.svg)](https://codecov.io/gl/Tuuux/galaxie-curses)

Galaxie Curses, The ToolKit
===========================
<div style="text-align:center"><img src ="https://gitlab.com/Tuuux/galaxie-curses/raw/master/docs/source/images/logo_galaxie.png" /></div>

Once upon a time, this project was hosted on a ancient platform called GitHub. Then came the Buyer.
The Buyer bought GitHub, willing to rule over its community.

I was not to sell, so here is the new home of "https://github.com/Tuuux/galaxie-curses".

The Project
-----------
**Galaxie Curses** alias **Le Truc Blue** (The Blue Thing) is a free software Tool Kit for the **NCurses** API.
It can be consider as a text based implementation of the famous **GTK+** Library (Or Ultra Inspired...).

Where ``implementation`` mean: ``Devellop a project from a documentation specs``.

Originally the project have start in 2016 when the author Jérôme.O have start to learn **Python** at home.

Then the lib is write in **Python**

```

**Pretty good**
<div style="text-align:center"><img src ="https://gitlab.com/Tuuux/galaxie-docs/raw/master/docs/source/images/result_01.png" /></div>

**Syntax coloration with css**
<div style="text-align:center"><img src ="https://gitlab.com/Tuuux/galaxie-docs/raw/master/docs/source/images/result_02.png" /></div>

Example
-------
```bash
glxdoc-md2html ./somewhere/README.md ./somewhere/else/README.html
```
**Help**
```bash
usage: glx-md2html [-h] [--lang LANG] [--charset CHARSET] source destination

Galaxie Docs

positional arguments:
  source             source file path
  destination        destination file path

optional arguments:
  -h, --help         show this help message and exit
  --lang LANG        HTTP_ACCEPT_LANGUAGE
  --charset CHARSET  character sets

Developed by Galaxie under GPLv3+ license

```

Features
--------
* CSS is include inside html file
* Code coloration
* EveryMarkDown extension is enable
* Defensive code style
* Singleton Thread safe
* Can be use as a class
* ``glxdoc-md2html`` command line interface

Roadmap
-------
Be the documents wrapper for **Galaxie-Curses** lib .

* create Html to Markdown converter
* create CVS to Markdown converter

Thanks
------
To everyone i have interest to it project, copy it, use it, diffuse it , and have fun ...

License
-------
GNU General Public License v3 or later (GPLv3+)
https://gitlab.com/Tuuux/galaxie-docs/blob/master/LICENSE