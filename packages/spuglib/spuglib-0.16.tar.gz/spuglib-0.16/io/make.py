#!/usr/local/bin/python

from makehack import hack0

modules = [
    ('HTTPServer', 'Proactor based HTTP server.'),
    ('LineReader', 'Wrapper class for file objects that keeps track of the '
                   'line number.'
     ),
    ('SSLServer', 
     'Proactor event handler wrapper to do SSL encryption of connections.'
     ),
    ('proactor', 'Implementation of the Proactor communication pattern.'),
    ('reactor', 'Implementation of the Reactor communication pattern.'),
]

hack0('io', modules)