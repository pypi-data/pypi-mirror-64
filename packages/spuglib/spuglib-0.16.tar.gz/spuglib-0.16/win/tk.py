# try to use tk 8.4 if it is available

try:
    from Tkinter84 import *
    from tkFont84 import *
except ImportError:
    try:
        from Tkinter import *
        from tkFont import *
    except ImportError:
        from tkinter import *
        from tkinter.font import *
