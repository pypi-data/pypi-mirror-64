===============
Flask Scaffold
===============
Package to create scaffolds for flask projects.

Installing
==========

To install the package, just run the following command::

  pip install flaskscaffold


Usage
=====

Help::

  flaskscaffold --help

To use simply create a directory for your project and then in the directory::

  flaskscaffold 

This will create the below folder structure:

::

    my_project
    ├── app.py
    ├── db.py
    ├── .gitignore
    ├── models         
    │   └── __init__.py
    ├── services         
    │   └── __init__.py
    ├── controllers         
    │   └── __init__.py
    └── tests



Or if you itend to buiild a web app::

  flaskscaffold --web

::

    my_project
    ├── app.py
    ├── db.py
    ├── .gitignore
    ├── models         
    │   └── __init__.py
    ├── services         
    │   └── __init__.py
    ├── controllers         
    │   └── __init__.py
    ├── static
    ├── templates
    └── tests

In addition to the file structure, boilerplate app.py and .gitignore is added.