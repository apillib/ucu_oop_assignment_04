import sys
from tkinter import *
from MyFrame import MyFrame 
from PIL import ImageTk, Image
import tksvg

def main(): 
    root = Tk() 
    root.geometry("700x600")
    #logo = ImageTk.PhotoImage(Image.open("icon.svg"))
    logo = tksvg.SvgImage(file="images\logo.svg")
    root.iconphoto(False, logo)
    app = MyFrame(root)
    root.mainloop()

if __name__ == "__main__": 
    sys.exit(int(main() or 0))