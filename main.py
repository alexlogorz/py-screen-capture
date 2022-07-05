from pynput import mouse
from dip import ImageProcessor
from dip import Algorithms
from dip import isInRange
from datetime import date
from db import DBManager
import tkinter as tk
import pyautogui

class Driver:
    def __init__(self):
        self.showCanvas = False
        # connect to db
        self.conn = DBManager('test.db')
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
        print("OCR Results: ", results)
        salesList = proc.extractSalesList(results)
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
        tuples = []
        for item in self.items:
            (itemText, itemPrice) = item
            stamp = date.today()
            tuples.append((itemText.get().replace(",", ""), itemPrice.get().replace(",", ""), stamp))
        self.conn.insertTuples(tuples)
        self.window.destroy()

    def closeCanvasWindow(self):
        self.window.destroy()

    def openResultsWindow(self, salesList):
        # items array used to store the (name, price) tuples 
        self.items = []
        self.window = tk.Tk()
        self.window.title("Edit Results")
        tk.Label(self.window, text = "Item Names").grid(row = 0,column = 0)
        tk.Label(self.window, text = "Item Prices").grid(row = 0,column = 1)
        for itemIdx in range(0, len(salesList[0])):
            itemNameText = tk.StringVar()
            itemPriceText = tk.StringVar()
            tk.Entry(self.window, textvariable=itemNameText).grid(row = itemIdx, column = 0, padx=5, pady=2, ipadx=3, ipady=3)
            tk.Entry(self.window, textvariable=itemPriceText).grid(row = itemIdx, column = 1, padx=5, pady=2, ipadx=3, ipady=3)
            itemNameText.set(salesList[0][itemIdx])
            itemPriceText.set(salesList[1][itemIdx]) if isInRange(salesList[1], itemIdx) else itemPriceText.set(0)
            self.items.append((itemNameText, itemPriceText))
        tk.Button(self.window, text ="Looks good!", command = self.submitResultsForm).grid(row = len(salesList[0]) + 1, column = 1, padx=5, pady=2, ipadx=3, ipady=3)
        self.window.mainloop()

def main():
    Driver()


if __name__ == '__main__':
    main()