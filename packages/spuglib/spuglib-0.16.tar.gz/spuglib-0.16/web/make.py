#!/usr/local/bin/python

from makehack import hack0

modules = [
    ('cgi', 'Tools for writing CGI programs'),
    ('cxml', 'Tools for manipulating a C-like form of XML.'),
    ('form', 'HTML form implementation classes.'),
    ('html', 'Classes for generating HTML (deprecated)'),
    ('htmlo', 'HTML object model.  HTML implemented on xmlo.'),
    ('wof', 'Web Object Framework'),
    ('xmlo', 'XML Objects.  DOM-like classes more oriented towards python.'),
    ('xparse', 'SAX based framework to facilitate XML parsing.'),
]

hack0('web', modules)