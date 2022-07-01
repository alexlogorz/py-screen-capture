from pynput import mouse
from dip import ImageProcessor
from dip import Algorithms
from dip import isInRange
import tkinter as tk
import pyautogui

class Utilities:
    def __init__(self):
        self.showCanvas = False
        # start the mouse listener
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()

    def takeScreenshot(self, event):
        savePath = r'C:\Users\alogo\py-screen-capture\screenshots\snippet.png'
        destPath = r'C:\Users\alogo\py-screen-capture\screenshots\modified.png'
        x0, y0, x1, y1 = self.canvas.coords(self.rect)
        self.toggleCanvas()
        pyautogui.screenshot(region=(x0, y0, x1 - x0, y1 - y0)).save(savePath)
        proc = ImageProcessor(savePath, destPath)
        results = proc.image2Text(Algorithms.DB_THRES)
        print("RESULTS: ", results)
        print("\n")
        salesList = proc.extractSalesList(results)
        print("SALES LIST: ", salesList)
        print("\n")
        self.openResultsWindow(salesList)

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
            self.closeCanvasWindow()
        else:
            self.showCanvas = True
            self.openCanvasWindow()
    
    def on_click(self, x, y, button, pressed):
        # detect right button release
        if button == button.right and pressed == False:
            self.toggleCanvas()
    
    def openCanvasWindow(self):
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

    def submitResultsForm(self):
        print('Submitted!')

    def closeCanvasWindow(self):
        self.window.destroy()

    def openResultsWindow(self, salesList):
        self.window = tk.Tk()
        self.window.title("Edit Results")
        # labels for the columns
        tk.Label(self.window ,text = "Item Names").grid(row = 0,column = 0)
        tk.Label(self.window ,text = "Item Prices").grid(row = 0,column = 1)
        # creates the grid system
        for itemIdx in range(0, len(salesList[1])):
            # text input for item name
            itemText = tk.StringVar()
            tk.Entry(self.window, textvariable=itemText).grid(row = itemIdx, column = 0, padx=5, pady=2, ipadx=3, ipady=3)
            itemText.set(salesList[1][itemIdx])
            # text input for item price
            priceText = tk.StringVar()
            tk.Entry(self.window, textvariable=priceText).grid(row = itemIdx, column = 1, padx=5, pady=2, ipadx=3, ipady=3)
            # fixes an out of range bug
            if isInRange(salesList[2], itemIdx):
                priceText.set(salesList[2][itemIdx])
            else:
                priceText.set(0)
        # text input for sellers name
        sellerText = tk.StringVar()
        tk.Entry(self.window, textvariable=sellerText).grid(row = len(salesList[1]) + 1, column = 0, padx=5, pady=5)
        sellerText.set(salesList[0])
        # submit button
        tk.Button(self.window, text ="Looks good!", command = self.submitResultsForm).grid(row = len(salesList[1]) + 1, column = 1, padx=5, pady=2, ipadx=3, ipady=3)
        self.window.mainloop()

def main():
    util = Utilities()


if __name__ == '__main__':
    main()