#!/usr/bin/python

from Tkinter import *

def onclick():
   pass

root = Tk()
text = Text(root)
text.insert(INSERT, "Hello.....")
#text.insert(END, "Bye Bye.....")
text.pack()

text.tag_add("here", "1.0", "1.4")

text.tag_config("here", background="yellow", foreground="blue")
#text.tag_config("start", background="black", foreground="green")
root.mainloop()
