episoder
========

Episoder is a tool to tell you about new episodes of your favourite TV shows. It
does so by parsing online TV episode guides.

Currently episoder can get data from epguides.com and thetvdb.com and tells you
whenever a new episode of a show listed on one of those sites is aired.

There is also a web-based version of episoder, called webisoder, which can be
used for free at webisoder.net.

Dependencies
------------

In order to use episoder, you will need python installed on your system. In
addition to the default distribution, the 'requests' and 'sqlalchemy' modules
are required.

Installation
------------

You can install episoder through pypi (using 'easy_install' or 'pip') or by
running 'setup.py' from the downloaded and extracted tarball.

Configuration
-------------

The configuration file at ~/.episoder contains your default settings for
episoder. After installing episoder, its manpage will help you with the
configuration.

Using episoder
--------------

To use episoder you will typically:

* Create a cron job to have your database rebuilt once a day by running
  `episoder update`
* Add `episoder` to your ~/.bashrc, ~/.bash_profile, /etc/bash.bashrc or
  /etc/profile if you want to see your upcoming shows every time you start a
  shell. Consult your shell's documentation to find out which file you want to
  use.
* Or run `episoder notify` at regular intervals to get your notifications by
  e-mail.
