#!python

import tkinter

from comicom import compiler
from comicom import comgui
from comicom import arguments

args = arguments.parse()

# Trigger the actual program....
if args.gui:
    window = tkinter.Tk()
    comgui = comgui.MainWindow(window)
    window.mainloop()
else:
    compiler.run(args)
