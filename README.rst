chain
=====

.. image:: https://img.shields.io/pypi/v/chain-py.svg
    :target: https://pypi.python.org/pypi/chain-py/
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/ajpen/chain.svg?branch=master
    :target: https://travis-ci.org/ajpen/chain
    :alt: Latest Travis CI build status

An expressive clean way to interact with REsTful APIs. It was inspired by `zmallen's pygraylog`_.

Chain is a small enhancement to the popular `requests`_ package. By referencing the endpoints as
attributes to the client, it effectively "chains" the endpoints together, building the target url.

Chain is an attempt to make REsTful API clients look more like python objects, by removing the
hardcoded URL strings in the code.

Chain uses the `requests`_ package as its http client, keeping its parameters and response objects.
If you already use `requests`_ as your http client, then adopting chain would be easy.

Usage
-----

Lets take for example `this API`_:

.. code-block:: pycon

    # create a new client for the API
    >>> import chain
    >>> blogs = chain.Client('http://jsonplaceholder.typicode.com')

    # if you want the posts:
    >>> response = blogs.get.posts()

    # the response is the response object from the requests package
    >>> print response.json()


Numbers and special characters are also supported using dictionary notation

.. code-block:: pycon

    # Get the first post
    >>> response = blogs.get.posts[1]()
    >>> print response.json()


chain parameters are requests.requests parameters:

.. code-block:: pycon

    # parameters are the same as requests.requests parameters
    >>> response = blogs.get.comments(params={'postId': '1'})
    >>> print response.json()

    >>> comment = {'postId': 1, 'id':501, 'name':'chain', 'email':'chain@code.com', 'body':'meh.'}
    >>> response = blogs.post.comments(json=comment)


Installation
------------
::

    pip install chain_py


Testing
-------
::

    python setup.py test

Or:
::

    tox


Compatibility
-------------

Works with Python version 2.7, 3.3, 3.4, 3.5 and 3.6


Licence
-------
MIT licensed. Requests is licensed by the Apache License. See full `LICENSE`_

Authors
-------

`chain` was written by `Anfernee Jervis <anferneejervis@gmail.com>`_.


.. _this API: https://jsonplaceholder.typicode.com/
.. _LICENSE: https://github.com/ajpen/chain/blob/master/LICENSE.md
.. _`zmallen's pygraylog`: https://github.com/zmallen/pygraylog
.. _requests: https://pypi.python.org/pypi/requests
