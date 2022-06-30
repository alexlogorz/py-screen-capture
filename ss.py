from tracemalloc import start
from pynput import mouse
import pyautogui
import tkinter as tk

import numpy as np
import datetime
import os, easyocr, math, cv2
import matplotlib.pyplot as plt

class ss:

    def __init__(self):
        self.window = tk.Tk()
        self.button1 = tk.Button(
            text="Enabled",
            width=25,
            height=5,
            bg="red",
            fg="black",
            command=self.enable_mouse_listener
        )
        self.button1.pack()
        self.button_on = False
        self.listener = None
        self.enable_mouse_listener()
        self.reader = easyocr.Reader(['en'], gpu=False)

        self.today = datetime.date.today().strftime("%d-%m-%Y")
        self.startingCoords = (0, 0)
        self.endingCoords = (0, 0)
        self.w = 0
        self.h = 0
        
        self.ss_pil = None
        self.ss_np = None
        self.results = None
        
        self.out_dir = 'screenshots'
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        self.window.mainloop()

    def take_screenshot(self):
        print('\nTook screenshot, running OCR...')

        self.ss_pil = pyautogui.screenshot(region=(self.startingCoords[0], self.startingCoords[1], self.endingCoords[0] - self.startingCoords[0], self.endingCoords[1] - self.startingCoords[1]))
        self.ss_np = np.array(self.ss_pil)
        self.ss_np = cv2.cvtColor(self.ss_np, cv2.COLOR_RGB2BGR)
        self.h, self.w = self.ss_np.shape[:2]
        self.center = (self.w // 2, self.h // 2)

    def get_results(self):
        self.results = self.reader.readtext(self.ss_np, detail=0, paragraph=False)

        print(self.results)
        for text in self.results:
            print(text)

        print('OCR Complete.')

    # This is the event listener for the on_click event
    def on_click(self, x, y, button, pressed):
        if button == button.right:
            if pressed:
                self.startingCoords = (x, y)

            else:
                self.endingCoords = (x, y)
                self.take_screenshot()
                self.get_results()

    def enable_mouse_listener(self):
        if not self.button_on:
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()
            self.button1.config(text="Enabled", bg="blue")
            self.button_on = True
        else:
            self.disable_mouse_listener()

    def disable_mouse_listener(self):
        self.listener.stop()
        self.button1.config(text="Disabled", bg="red")
        self.button_on = False

def main():
    ss()

if __name__ == '__main__':
    main()