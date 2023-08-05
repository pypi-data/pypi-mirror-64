
.. |travis| image:: https://travis-ci.org/proofit404/service-factory.png
    :target: https://travis-ci.org/proofit404/service-factory
    :alt: Build Status

.. |coveralls| image:: https://coveralls.io/repos/proofit404/service-factory/badge.png
    :target: https://coveralls.io/r/proofit404/service-factory
    :alt: Coverage Status

.. |requires| image:: https://requires.io/github/proofit404/service-factory/requirements.svg
    :target: https://requires.io/github/proofit404/service-factory/requirements
    :alt: Requirements Status

.. |landscape| image:: https://landscape.io/github/proofit404/service-factory/master/landscape.svg
    :target: https://landscape.io/github/proofit404/service-factory/master
    :alt: Code Health

===============
service-factory
===============

|travis| |coveralls| |requires| |landscape|

JSON RPC service factory for Python.

Usage
-----

Service factory in a nutshell:

.. code:: python

    from service_factory import service_factory

    def add(one, two):
        """Add two numbers."""
        return one + two

    def mul(one, two):
        """Multiply two numbers."""
        return one * two

    app = [add, mul]

    if __name__ == '__main__':
        service_factory(app, host='localhost', port=0)

Run this as usual python file:

.. code:: bash

    $ python calc.py
    service factory starts at port 9001

See it works:

.. code:: bash

    $ curl -X POST -d '{"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1}' -H 'Content-Type:application/json;' http://localhost:9001/

You can use any callable list from arbitrary module to run your
application:

.. code:: bash

    $ python -m service_factory calc:app --host=localhost --port=auto
    # or
    $ service_factory calc:app --host=localhost --port=auto

TODO
----

* process all errors codes
* batch processing
* notifications
* WSGI provider
* tornado provider
* aiohttp provider
* --port-file option
* console entry point
* make providers act as context managers
* ``user_error(code, message, data=None)``
* WSGI authorization
* sphinx docs
* Django user permissions for rpc method
* Celery service implementation
* RQ service implementation
