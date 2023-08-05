#!/usr/local/bin/python

from makehack import hack0

modules = [
    ('Controls', 'Compound control classes.'),
    ('FileBrowser', 'A file browser implementation'),
    ('StatefulCheckbutton', 'A checkbutton control which tracks its own state.'),
    ('StdWin', 'Commonly used toplevel windows.'),
    ('WinStream', 'A text window that can be used like a file object.'),
    ('bind', 'Class to simplify binding keys to methods.'),
    ('scrtext', 'A text control with scrollbars.'),
]

hack0('win', modules)