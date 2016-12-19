# HTTP Server

This is an implementation of a socket server.
In this implementation, we create a server and a client.
If the client request a file contained in the root, the server will serve it.
If the client doesn't request properly, the server will respond appropriately.

We also implemented a concurrency module using Gevent that will allow us to handle multiple requests.


## Contains:
    - Modules:
        - *client.py*
        - *server.py*
        - *concurrency.py*
    - Tests:
        - *test_unit.py*
        - *test_functional.py*

## Use:
We have been having trouble with entry points.
Currently you can clone this repo and type `python3 server <port>` to run the server.
You can then open your browser localhost and request files from the webroot.
Alternatively you can open the client in another terminal and type `python3 client <request>`, request being a valid HTTP GET request.


## Coverage:

```sh
---------- coverage: platform darwin, python 2.7.10-final-0 ----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
src/client.py                      42      0   100%
src/concurrency.py                  7      7     0%   2-23
src/server.py                     111     20    82%   33-48, 95, 98, 100, 171
src/tests/__init__.py               0      0   100%
src/tests/test_concurrency.py       0      0   100%
src/tests/test_functional.py       21      0   100%
src/tests/test_unit.py             46      0   100%
-------------------------------------------------------------
TOTAL                             227     27    88%
```

## Authors:
Ford Fowler and Maelle Vance