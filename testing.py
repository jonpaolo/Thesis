import cv2
import numpy as np
import threading
from tkinter import *
from PIL import Image, ImageTk



def StandByModeButton():
    button_label = Label(f1, text="Stand By Mode", compound="c", font=("Arial", 16), bg="white", fg="black")
    button_label.pack(pady=5, side=BOTTOM)

    # Associate the button with the button_clicked function
    button_label.bind("<Button-1>", lambda e: button_clicked(button_label))

def ForwardButton():
    foward_button = Label(L1, text="Forward", compound="c", font=("Arial", 16),bg='#ab23ff')
    foward_button.pack(pady = 5, side=TOP)
    foward_button.bind("<Button-2>", lambda e: button_clicked(foward_button))


def TleftButton():
    left_button = Label(L1, text="Left", compound="c", font=("Arial", 16), bg='#ab23ff')
    left_button.pack(pady = 5, side=LEFT)
    left_button.bind("<Button-3>", lambda e: button_clicked())

def TrightButton():
    button_label = Label(L1, text="Right", compound="c", font=("Arial", 16), bg='#ab23ff')
    button_label.pack(pady = 5, side=RIGHT)
    button_label.bind("<Button-4>", lambda e: button_clicked(button_label))

# Function to be called when the button is clicked
def button_clicked(button):
    global mode
    if mode == "Stand By Mode":
        mode = "Driving Mode"
        button.config(text=mode)
    else:  # mode is "Driving Mode"
        mode = "Stand By Mode"
        button.config(text=mode)
    print("Button clicked! Current mode:", mode)

# Create the root window
root = Tk()
root.geometry("1280x720")  # Set the dimensions of the GUI window\

# Create a frame for the camera grid
f1 = LabelFrame(root)
f1.pack()

# Create a label for the camera feed
L1 = Label(f1)
L1.pack()

# Create a frame for the button
f2 = Frame(root, bg="white")
f2.pack()

# Create transparent box buttons with text labels
root.wm_attributes('-transparentcolor', '#ab23ff')

StandByModeButton()
ForwardButton()
TleftButton()
TrightButton()

root.configure(bg="white")
cap = cv2.VideoCapture(0)

new_width = 1080  # Define the desired width for the captured frame
new_height = 720  # Define the desired height for the captured frame

mode = "Stand By Mode"  # Initialize the mode

while True:
    ret = False
    if mode in ["Driving Mode"]:  # Check if the mode is "Driving Mode"   
        ret, frame = cap.read()

    if ret:
        # Resize the frame to the desired dimensions
        frame = cv2.resize(frame, (new_width, new_height))
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
        L1['image'] = img
    root.update()

    if mode in ["Stand By Mode"]:  # Check if the mode is "Stand By Mode"
        L1.pack_forget()  # Hide the camera feed if in "Stand By Mode"
    else:
        L1.pack()  # Show the camera feed if in "Driving Mode" or "Forward"

# Set the desired dimensions for the captured frame
new_width = 1080
new_height = 720

mode = "Stand By Mode"  # Initialize the mode

# Define the on_closing function before binding it
def on_closing():
    # Close the serial connection when exiting the application
    ser.close()
    root.destroy()

# Bind the exit button to on_closing
root.protocol("WM_DELETE_WINDOW", on_closing)
def read_serial():
    while True:
        try:
            data = ser.readline().decode().strip()  # Read and decode data from the serial port
            print("Arduino Output:", data)  # Print the received data to the terminal
        except Exception as e:
            print("Error reading from serial port:", e)

# Create a separate thread for reading serial data
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

while True:
    ret, frame = cap.read()
    if ret:
        # Resize the frame to the desired dimensions
        frame = cv2.resize(frame, (new_width, new_height))

        # Convert the frame to RGB and create an ImageTk object
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

        # Update the image in the label and refresh the GUI window
        L1['image'] = img
        root.update()

cap.release()
cv2.destroyAllWindows()