from pynput import mouse
import tkinter as tk
import pyautogui

class Utilities:
    def __init__(self):
        self.showCanvas = False
        # start the mouse listener
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()

    def takeScreenshot(self, event):
        print('took screenshot')
        x0, y0, x1, y1 = self.canvas.coords(self.rect)
        self.toggleCanvas()
        pyautogui.screenshot(region=(x0, y0, x1 - x0, y1 - y0)).save(r'C:\Users\alogo\py-screen-capture\screenshots\snippet.png')

    def setRect(self, event):
        # creates a rect on the current mouse position
        self.rect = self.canvas.create_rectangle(event.x, event.y, event.x + 1, event.y + 1, outline='red', fill='')

    def resizeRect(self, event):
        # set new rect coords
        x0, y0, x1, y1 = self.canvas.coords(self.rect)
        self.canvas.coords(self.rect, x0, y0, event.x, event.y)

    def toggleCanvas(self):
        if self.showCanvas:
            self.showCanvas = False
            self.closeWindow()
        else:
            self.showCanvas = True
            self.openWindow()
    
    def on_click(self, x, y, button, pressed):
        # detect right button release
        if button == button.right and pressed == False:
            self.toggleCanvas()
    
    def openWindow(self):
        # configure the window
        self.window = tk.Tk()
        self.window.attributes('-topmost', True)
        self.window.attributes('-fullscreen', True)     
        self.window.attributes('-alpha',0.5)
        # configure the canvas
        self.canvas = tk.Canvas(self.window, bg='white')
        self.canvas.bind('<Button-1>', self.setRect)
        self.canvas.bind('<ButtonRelease-1>', self.takeScreenshot)
        self.canvas.bind('<B1-Motion>', self.resizeRect)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.window.mainloop()

    def closeWindow(self):
        self.window.destroy()

def main():
    util = Utilities()
    


if __name__ == '__main__':
    main()