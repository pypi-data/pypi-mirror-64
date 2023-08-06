# dj-inmemorystorage

[![image](https://travis-ci.org/waveaccounting/dj-inmemorystorage.png?branch=master)](https://travis-ci.org/waveaccounting/dj-inmemorystorage)

[![PyPI](https://img.shields.io/pypi/v/dj-inmemorystorage.svg)](https://pypi.python.org/pypi/dj-inmemorystorage)

An in-memory data storage backend for Django.

Compatible with Django's [storage
API](https://docs.djangoproject.com/en/dev/ref/files/storage/).

# Supported Versions

  - Python 2.7 with Django 1.11
  - Python 3.5/3.6/3.7 with Django 1.11+
  - Python 3.8 with Django 2.2+

In general, we follow [Python's supported
versions](https://devguide.python.org/#status-of-python-branches) and
[Django's supported
versions](https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django).
Any major change in version support will be released as a new major
version.

# Usage

In your test settings file, add

``` python
DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
```

By default, the `InMemoryStorage` backend is non-persistant, meaning
that writes to it from one section of your code will not be present when
reading from another section of your code, unless both are sharing the
same instance of the storage backend.

If you need your storage to persist, you can add the following to your
settings.

``` python
INMEMORYSTORAGE_PERSIST = True
```

# Differences

This library is based on
[django-inmemorystorage](https://github.com/codysoyland/django-inmemorystorage)
by Cody Soyland, with
[modifications](https://github.com/SeanHayes/django-inmemorystorage)
made by Seán Hayes with support for the `url` method, with [additional
support](https://github.com/Vostopia/django-inmemorystorage) from Tore
Birkeland for writing to the file.

Wave's modifications include packaging, and test modifications such that
`python setup.py test` works. This version also bumps the version to
`1.0.0` and renames it to dj-inmemorystorage such that it doesn't
conflict on PyPI.

The biggest difference is that this package works with Django 1.4 now
(previously only 1.5+). It also supports Python 2.6/2.7 with Django
1.4+, Python 3.2/3.3/3.4 with Django 1.5+ and Python 3.5/3.6 with Django
1.7+.

# Contributing

1.  Ensure that you open a pull request
2.  All feature additions/bug fixes MUST include tests
