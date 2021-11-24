# This is about all it requires to write a wish shell in Python!

import _tkinter
import os

tk = _tkinter.create(os.environ['DISPLAY'], 'wish', 'Tk', 1)
tk.call('update')

cmd = ''

while 1:
    if cmd: prompt = ''
    else: prompt = '% '
    try:
        line = raw_input(prompt)
    except EOFError:
        break
    cmd = cmd + (line + '\n')
    if tk.getboolean(tk.call('info', 'complete', cmd)):
        tk.record(line)
        try:
            result = tk.call('eval', cmd)
        except _tkinter.TclError, msg:
            print 'TclError:', msg
        else:
            if result: print result
        cmd = ''
