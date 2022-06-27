from tracemalloc import start
from pynput import mouse
import pyautogui
import tkinter as tk

window = tk.Tk()

def take_screenshot(startingCoords, endingCoords):
    print('took screenshot')
    pyautogui.screenshot(region=(startingCoords[0], startingCoords[1], endingCoords[0] - startingCoords[0], endingCoords[1] - startingCoords[1])).save(r'C:\Users\alogo\OneDrive\Desktop\py-screen-capture\screenshots\snippet.png')
    disable_mouse_listener()

# This is the event listener for the on_click event
def on_click(x, y, button, pressed):
    global startingCoords
    global endingCoords
    if button == button.left:
        if pressed:
            startingCoords = (x, y)
        else:
            endingCoords = (x, y)
            take_screenshot(startingCoords, endingCoords)


def enable_mouse_listener():
    global listener
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    button1.config(text="listener enabled", bg="blue")

def disable_mouse_listener():
    listener.stop()
    button1.config(text="listener disabled", bg="red")

# The button configuration
button1 = tk.Button(
    text="listener is disabled",
    width=25,
    height=5,
    bg="red",
    fg="white",
    command=enable_mouse_listener
)


# This adds the button to the gui window
button1.pack()

# The main event loop for the window. Listens for events like button clicks etc
window.mainloop()