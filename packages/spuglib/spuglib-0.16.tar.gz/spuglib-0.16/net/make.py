#!/usr/local/bin/python

from makehack import hack0

modules = \
   [ 
   ('sendmail', 'Module containing classes to do outgoing mail processing'),
   ('socks', 'Module for doing SOCKS connections')
   ]

hack0('net', modules)