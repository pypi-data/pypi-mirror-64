Custom User-Agent
=================

Why do we need it?
------------------

As we need to be one in a middle of connection to a webserver, the custom user agent is there for that!

How does it work?
-----------------

We set the custom user-agent everytime we request something with the :code:`http` and :code:`https` protocols.

How to use it?
--------------

Simply give us your custom user agent

::

    user_agent:
        browser: chrome
        platform: linux
        custom: "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"

into your personal :code:`.PyFunceble.yaml` or use the :code:`--user-agent` argument from the CLI.

What if we don't give a custom User-Agent?
------------------------------------------

If you don't set a custom User-Agent, we will try to get the latest one for the chosen
browser and platform.
