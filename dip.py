import cv2
from cv2 import scaleAdd
import easyocr
import enum
import re

class Algorithms(enum.Enum):
        BINARIZE = 0
        DB_THRES = 1
        NONE = 2

def isInRange(array, index):
        if 0 <= index <= len(array) - 1:
            return True
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
                if (180 <= pixel[0] <= 255 and 180 <= pixel[1] <= 255 and 180 <= pixel[2] <= 255) or (pixel[0] == 0 and 126 <= pixel[1] <= 153 and pixel[2] == 0) or (210 <= pixel[0] <= 255 and 42 <= pixel[1] <= 51 and 42 <= pixel[2] <= 51):
                    image[row,col] = [0, 0, 0]
                else:
                    image[row,col] = [255, 255, 255]
        return image

    def saveImage(self, img):
        cv2.imwrite(self.destPath, img)

    def image2Text(self):
        result = self.reader.readtext(self.srcPath, detail = 0, paragraph=False)
        return result
    
    # overloaded to specify preprocessing
    def image2Text(self, algo):
        if(algo == Algorithms.BINARIZE):
            bin_img = self.binarize(210)
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
        seller = results[0]
        itemNames = []
        itemPrices = []
        salesList = results[results.index('Sale List') + 1:len(results)]
        
        print("SUBARRAY LIST: ", salesList)
        print("\n")

        for currentItemIdx in range(0, len(salesList)):
            currentItem = salesList[currentItemIdx]
            # match item price
            if re.search("[.,]", currentItem):
                itemPrices.append(currentItem)
            # match item name
            else:
                # an item tier
                if(re.search("^\+\d{1,2}$", currentItem)):
                    pass
                else:
                    # just a guard to protect against out of range error
                    if isInRange(salesList, currentItemIdx + 1):
                        # if next item is a tier then it belongs to this items name
                        nextItem = salesList[currentItemIdx + 1]
                        if re.search("^\+\d{1,2}$", nextItem):
                            itemNames.append(currentItem + " " + nextItem)
                        else:
                            itemNames.append(currentItem)
                    else:
                        # no need to worry about tiers here since there is no next item
                        itemNames.append(currentItem)

        return [seller, itemNames, itemPrices]


