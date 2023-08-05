#!/usr/local/bin/python

from makehack import hack0

modules = \
   [
   ('StdFormatter', 'Contains base class functionality useful to all NML '
                    'formatters.'
    ),
   ('block', 'Recursive NML block classes: these are the data representations '
             'of NML documents.'
    ),
             
   ('html', 'Module for writing NML out as HTML'),
   ('docbook', 'Module for writing NML out as Docbook'),
   ('parse', 'NML parser.'),
   ('tcltext', 'Module for formatting NML into a TCL text control.'),
   ('troff', 'Module for writing NML as TROFF.'),
   ]

hack0('nml', modules)

