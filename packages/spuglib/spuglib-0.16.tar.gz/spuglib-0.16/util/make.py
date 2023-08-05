#!/usr/local/bin/python

from makehack import hack0

modules = \
   [ 
   ('AppEnv', 'Support for application specific configuration files.'),
   ('ComLine', 'Command line argument processing classes.'),
   ('Date', 'Date processing class.'),
   ('DateRange', 'Date range processing class.'),
   ('DateTime', 'Date and time processing class.'),
   ('StdError', 'General exceptions and error processing classes.'),
   ('ez', 'Quick and dirty python hacks.'),
   ('log', 'Logging interface (front end to different types of loggers'),
   ('process', 'Classes for safely invoking and interacting with child '
	       'processes'),
   ('quickle', 'Simple wrapper commands to pickle and unpickle objects '
               'directly to and from files.'),
   ('shell', 'Functions to make python more like bash'),
   ('tok', 'A simple lexical tokenizer.'),
   ]

hack0('util', modules)
