import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title("testing")
root.geometry("1280x70")

def StandByButton():
    button_label= Label(root, text ="Stand by Mode", compound="c", font=("Arial", 16), fg="black")
    button_label.pack(pady=10, side=BOTTOM)
    button_label.bind("<Button-1>", lambda e: button_clicked(button_label))

def ForwardButton():
    button_label = Label(root, text="Forward", compound="c", font=("Arial", 16), fg="black")
    button_label.pack(pady=10, side=TOP)
    button_label.bind("<Button-2>", lambda e: button_clicked(button_label))

def TleftButton():
    button_label = Label(root, text="Left", compound="c", font=("Arial", 16), fg="black")
    button_label.pack(pady = 10, side=LEFT)
    button_label.bind("<Button-4>", lambda e: button_clicked(button_label))

def TrightButton():
    button_label = Label(root, text="Right", compound="c", font=("Arial", 16), fg="black")
    button_label.pack(pady=10, side=RIGHT)
    button_label.bind("<Button-5>", lambda e: button_clicked(button_label))

def button_clicked(button):
    global mode
    if mode == "Stand By Mode":
        mode = "Driving Mode"
        button.config(text=mode)
    else:  # mode is "Driving Mode"
        mode = "Stand By Mode"
        button.config(text=mode)
    print("Button clicked! Current mode:", mode)

StandByButton()
ForwardButton()
TleftButton()
TrightButton()

root.mainloop()