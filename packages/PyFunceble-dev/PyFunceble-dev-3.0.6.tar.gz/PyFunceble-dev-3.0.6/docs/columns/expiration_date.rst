Expiration Date
===============

There's two possible output for this column.

Unknown
-------

:code:`Unknown` is returned when we could not extract the expiration date from :func:`~PyFunceble.lookup.whois.Whois` outputs.

A date
------

Only if we could extract the expiration date from :func:`~PyFunceble.lookup.whois.Whois`, the date becomes formatted like :code:`02-jan-2017`.
