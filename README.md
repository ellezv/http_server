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
        - *test_concurrency.py*

## Use:
We have been having trouble with entry points.
Currently you can clone this repo and type `python3 server <port>` to run the server.
You can then open your browser localhost and request files from the webroot.
Alternatively you can open the client in another terminal and type `python3 client <request>`, request being a valid HTTP GET request.


## Coverage:

```sh
---------- coverage: platform darwin, python 3.5.2-final-0 -----------
Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
src/client.py                 18     10    44%   13-20, 23-24
src/server.py                 14     14     0%   2-20
src/tests/__init__.py          0      0   100%
src/tests/test_server.py       4      0   100%
--------------------------------------------------------
TOTAL                         36     24    33%
```

## Authors:
Ford Fowler and Maelle Vance