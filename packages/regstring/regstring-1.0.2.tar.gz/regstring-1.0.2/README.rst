pyregstring
===========

A a simple lib to create string by regex

example
-------

.. code:: python

   from regstring import pyregstring

   r = b"(?<action>\\w+)\\s(?<url>\\S+)\\s(?<version>\\S+)\r\n"

   rs = pyregstring()

   if (rs.parse_regex(r)):
       rs.set(b"action", b"GET")
       rs.set(b"url", b"/test")
       rs.set(b"version", b"HTTP/1.1")
       print(rs.to_bytes())
       print(rs.names())
       print(rs.size())

.. code:: python

   b'GET /test HTTP/1.1\r\n'
   [b'action', b'url', b'version']
   20
