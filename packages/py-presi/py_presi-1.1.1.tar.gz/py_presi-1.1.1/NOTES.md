# Why should you use a setup.py?

- Namespace in imports
- Easier to select tests for coverage
- Your editor can easier find files
- No name conflicts for e.g, api
- No crazy sys.path hacks or file not found

# How is a package structured?

- Repo should be called like package
- Subfolder should be called like package
- Name in setup.py should be called like package
- Remember - are converted to _
- Install `pip install git+https://gitlab.com/delijati/py-presi` is possible

# What is virtualenv, pip, pipenv, setuptools, pypi?

- virtualenv to copy python and isolate env
- pip to install packages more advanced then setuptools
- pipenv a combination of both
- pypi the cheesshop of python aka artifact repo

# How should package be versioned?

The version is immutable and it should be in DEV, QA, PROD always the same
version. 

How to track changes?

- Simply do it, it su.. but needs to be done
- git log is to verbose to be used

# Why use libraries and not put all code into the repo?

e.g. https://github.com/marshmallow-code/marshmallow

# Why should all code look the same?

Guido tell them

# TODO

Add proper twine upload https://medium.com/@pypripackages/using-gitlab-pipelines-to-deploy-python-packages-in-production-and-staging-environments-8ab7dc979274
