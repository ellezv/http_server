# HTTP Server

This is an implementation of a socket echo server.  
In this implementation, we create a server and a client. The client will send a message to the server will respond back with a header containing 200 ok response code.

Right now unicode is giving us trouble but it will be compatible with python 2 and 3. 


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