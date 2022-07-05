import cv2
import easyocr
import enum
import re
from math import floor

class Algorithms(enum.Enum):
        BINARIZE = 0
        DB_THRES = 1
        NONE = 2
class Channel(enum.Enum):
    B = 0
    G = 1
    R = 2

# some helper methods
def isInRange(array, index):
        if 0 <= index <= len(array) - 1:
            return True
        return False

def isPrice(currentItem):
    if re.search("^\d\d\d$", currentItem) or re.search("^[0-9,]*$", currentItem):
        return True
    else:
        return False
        

class ImageProcessor:
    def __init__(self, srcPath, destPath):
        self.srcPath = srcPath
        self.destPath = destPath
        # initialize easyocr
        self.reader = easyocr.Reader(['en'], gpu=False)

    def binarize(self, threshold):
        gray_img = cv2.imread(self.srcPath, cv2.IMREAD_GRAYSCALE)
        image = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)[1]
        return image

    def doubleThres(self):
        image = cv2.imread(self.srcPath)
        for row in range(0, image.shape[0]):
            for col in range(0, image.shape[1]):
                pixel = image[row,col]
                if (204 <= pixel[0] <= 255 and 204 <= pixel[1] <= 255 and 204 <= pixel[2] <= 255) or (pixel[0] == 0 and 122 <= pixel[1] <= 153 and pixel[2] == 0) or (204 <= pixel[0] <= 255 and 41 <= pixel[1] <= 51 and 41 <= pixel[2] <= 51):
                    image[row,col] = [0, 0, 0]
                else:
                    image[row,col] = [255, 255, 255]
        return image

    def saveImage(self, img):
        cv2.imwrite(self.destPath, img)

    def image2Text(self, algo):
        if(algo == Algorithms.BINARIZE):
            bin_img = self.binarize(127)
            self.saveImage(bin_img)
            result = self.reader.readtext(self.destPath, detail = 0, paragraph=False)
        elif(algo == Algorithms.DB_THRES):
            db_thres = self.doubleThres()
            self.saveImage(db_thres)
            result = self.reader.readtext(self.destPath, detail = 0, paragraph=False)
        else:
            result = self.reader.readtext(self.srcPath, detail = 0, paragraph=False)
        return result
   

    def extractSalesList(self, results):
        itemNames = []
        itemPrices = []
        for currentIdx in range(0, len(results)):
            currentItem = results[currentIdx]
            if isPrice(currentItem):
                itemPrices.append(currentItem)
            else:
                if isInRange(results, currentIdx + 1):
                    nextItem = results[currentIdx + 1]
                    if re.search("^\+\d{1,2}$", nextItem) or re.search("^\d% *\)$", nextItem):
                        itemNames.append(currentItem + " " + nextItem)
                    elif re.search("^\+\d{1,2}$", currentItem) or re.search("^\d% \)$", currentItem):
                        pass
                    else:
                        itemNames.append(currentItem)
                else:
                    itemNames.append(currentItem)
        print("Sales List: ", [itemNames, itemPrices])
        return [itemNames, itemPrices]


