import cv2
import easyocr

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

    def doubleThreshold(self):
        image = cv2.imread(self.srcPath)
        for row in range(0, image.shape[0]):
            for col in range(0, image.shape[1]):
                pixel = image[row,col]
                if (188 <= pixel[0] <= 255 and 188 <= pixel[1] <= 255 and 188 <= pixel[2] <= 255) or (0 <= pixel[0] <= 1 and 56 <= pixel[1] <= 145 and 0 <= pixel[2] <= 1) or (93 <= pixel[0] <= 249 and 19 <= pixel[1] <= 50 and 19 <= pixel[2] <= 50):
                    image[row,col] = [0, 0, 0]
                else:
                    image[row,col] = [255, 255, 255]
        return image

    def saveImage(self, img):
        cv2.imwrite(self.destPath, img)

    def image2Text(self):
        result = self.reader.readtext(self.srcPath, detail = 0, paragraph=False)
        return result

    def extractSalesList(self, results):
        seller = results[0]
        itemNames = []
        itemPrices = []

        for i in range(results.index('Chat') + 1, len(results) - 1):
            currentItem = results[i]
            if "," in currentItem or "." in currentItem:
                itemPrices.append(currentItem)
            else:
                itemNames.append(currentItem)

        return [seller, itemNames, itemPrices]

