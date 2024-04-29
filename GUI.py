import cv2
import numpy as np
import serial
import threading
from tkinter import *
from PIL import Image, ImageTk
import tobii_library

# Initialize Arduino
serial_port = "COM3"
baud_rate = 115200
ser = serial.Serial(serial_port, baud_rate)

#Find Eye Tracker
found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]

#Defining GUI Buttons
def StandByModeButton():
    button_label = Label(f2, text="Stand By Mode", compound="c", font=("Arial", 16), bg="white", fg="black")
    button_label.pack(pady=20)
    button_label.bind("<Button-1>", lambda e: button_clicked(button_label))

def ForwardButton():
    button_label = Label(f2, text="Forward", compound="c", font=("Arial", 16), bg="white", fg="black")
    button_label.pack(pady=500)
    button_label.bind("<Button-2>", lambda e: button_clicked(button_label))

def BackwardButton():
    button_label = Label(f2, text="Backward", compound="c", font=("Arial", 16), bg="white", fg="black")
    button_label.pack(pady=500)
    button_label.bind("<Button-3>", lambda e: button_clicked(button_label))

def TleftButton():
    button_label = Label(f2, text="Left", compound="c", font=("Arial", 16), bg="white", fg="black")
    button_label.pack(pady=500)
    button_label.bind("<Button-4>", lambda e: button_clicked(button_label))

def TrightButton():
    button_label = Label(f2, text="Right", compound="c", font=("Arial", 16), bg="white", fg="black")
    button_label.pack(pady=500)
    button_label.bind("<Button-5>", lambda e: button_clicked(button_label))

# Function to be called when the button is clicked
def button_clicked(button):
    global mode
    if mode == "Stand By Mode":
        mode = "Driving Mode"
        button.config(text=mode)
        ser.write("On".encode())
    else:
        mode = "Stand By Mode"
        button.config(text=mode)
        ser.write("Off".encode())
    print("Button clicked! Current mode:", mode)

    # Start reading Tobii eye-tracking data
def read_tobii_data(gaze_data):
# Print gaze points of left and right eye
    print("Left eye: ({gaze_left_eye}) \t Right eye: ({gaze_right_eye})".format(
        gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
        gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))

# Start Gaze Tracking
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

# Create the root window
root = Tk()
root.geometry("1280x720")

root.mainloop()
# Create the root window
root = Tk()
root.geometry("1280x720")  # Set the dimensions of the GUI window

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
StandByModeButton()
ForwardButton()
BackwardButton()
TleftButton()
TrightButton()

root.configure(bg="white")
cap = cv2.VideoCapture(0)

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