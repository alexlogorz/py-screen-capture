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
            text="listener is disabled",
            width=25,
            height=5,
            bg="red",
            fg="black",
            command=self.enable_mouse_listener
        )
        self.button1.pack()
        self.button_on = False

        self.startingCoords = (0, 0)
        self.endingCoords = (0, 0)
        self.listener = None
        self.ss_pil = None
        self.ss_np = None
        self.today = datetime.date.today().strftime("%d-%m-%Y")

        self.reader = easyocr.Reader(['en'], gpu=False)
        self.results = None
        self.w = 0
        self.h = 0
        
        self.out_dir = 'screenshots'
        if not os.path.exists(self.out_dir):
            os.makedirs(self.out_dir)

        self.window.mainloop()

    def take_screenshot(self):
        print('\nTook screenshot, running OCR...')
        self.ss_pil = pyautogui.screenshot(region=(self.startingCoords[0], self.startingCoords[1], self.endingCoords[0] - self.startingCoords[0], self.endingCoords[1] - self.startingCoords[1]))
        # self.ss_pil = pyautogui.screenshot()
        # self.ss_np = np.array(self.ss_pil)
        self.ss_np = np.array(self.ss_pil)
        self.ss_np = cv2.cvtColor(self.ss_np, cv2.COLOR_RGB2BGR)
        self.h, self.w = self.ss_np.shape[:2]
        self.center = (self.w // 2, self.h // 2)
        # print(f'image size: {self.h}, {self.w}')
        # print(f'ss type: {type(ss)}')
        # self.disable_mouse_listener()

        # ratio_w = 0.09
        # ratio_h = 0.05
        # pixel_diff_w = self.w * ratio_w
        # pixel_diff_h = self.h * ratio_h
        # left = int(math.floor(self.center[0] - pixel_diff_w))
        # right = int(math.ceil(self.center[0] + pixel_diff_w))
        # top = int(math.ceil(pixel_diff_h))
        # bottom = int(math.floor(self.h - pixel_diff_h))
        # self.ss_np = self.ss_np[top:bottom, left:right, ...]

        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        # flags = cv2.KMEANS_RANDOM_CENTERS
        # pv = np.float32(self.ss_np.reshape((-1, 3)))
        # compactness, labels, centers = cv2.kmeans(pv, 2, None, criteria, 10, flags)
        # centers = np.uint8(centers)
        # seg = centers[labels.flatten()].reshape(self.ss_np.shape)
        # cv2.imwrite('test_seg.png', seg)

        # print(top, bottom, self.ss_np.shape)
        # cv2.imwrite('test.png', self.ss_np)
        

    # This is the event listener for the on_click event
    def on_click(self, x, y, button, pressed):
        if button == button.right:
            if pressed:
                self.startingCoords = (x, y)

            else:
                self.endingCoords = (x, y)
                self.take_screenshot()
                results = self.reader.readtext(self.ss_np, detail=0, paragraph=True)

                results = [s.replace('.', ',') for s in results]
                results = [s.replace(',,', ',') for s in results]
                print(results)

                # for bbox, text, prob in self.results:
                #     # if 'Private Shop' in text:
                #     #     print(text)
                #     print(text)

                print('OCR Complete.')


    def enable_mouse_listener(self):
        if not self.button_on:
            self.listener = mouse.Listener(on_click=self.on_click)
            self.listener.start()
            self.button1.config(text="listener enabled", bg="blue")
            self.button_on = True
        else:
            self.disable_mouse_listener()
            self.button_on = False

    def disable_mouse_listener(self):
        self.listener.stop()
        self.button1.config(text="listener disabled", bg="red")

def main():

    # window = tk.Tk()

    # The button configuration
    # button1 = tk.Button(
    #     text="listener is disabled",
    #     width=25,
    #     height=5,
    #     bg="red",
    #     fg="white",
    #     command=enable_mouse_listener
    # )


    # This adds the button to the gui window
    # button1.pack()

    # The main event loop for the window. Listens for events like button clicks etc
    # window.mainloop()

    ss_0 = ss()

if __name__ == '__main__':
    main()