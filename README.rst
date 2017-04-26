chain
=====

.. image:: https://img.shields.io/pypi/v/chain.svg
    :target: https://pypi.python.org/ajpen/chain
    :alt: Latest PyPI version

An expressive clean way to interact with RESTful APIs. It was inspired by `zmallen's pygraylog`_.

This project is very unstable and under active development.

Usage
-----

Lets take for example `this API:`_

.. code-block:: pycon

    # create a new client for the API
    >>> import chain
    >>> blogs = chain.Client('jsonplaceholder.typicode.com')

    # if you want the posts:
    >>> response = blogs.get.posts()

    # the response object is raw now but will receive features later!
    >>> print response.raw_response.read()

What about queries?

.. code-block:: pycon

    >>> response = blogs.get.comments({'postId': '1'})
    >>> print response.raw_response.read()


Installation
------------
::

    git clone https://github.com/ajpen/chain


Requirements
^^^^^^^^^^^^

Nothing so far.

Compatibility
-------------

(Barely!) Tested with 2.7


Licence
-------
MIT licensed. See full `LICENSE`_

Authors
-------

`chain` was written by `Anfernee Jervis <anferneejervis@gmail.com>`_.


.. _`this API:`: https://jsonplaceholder.typicode.com/
.. _LICENSE: https://github.com/ajpen/chain/blob/master/LICENSE.md
.. _`zmallen's pygraylog`: https://github.com/zmallen/pygraylog