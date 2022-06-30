import cv2

class ImageProcessor:
    def __init__(self, filePath):
        self.filePath = filePath

    def binarize(self, threshold):
        gray_img = cv2.imread(self.filePath, cv2.IMREAD_GRAYSCALE)
        tmp = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY)[1]
        print('binarizing img')
        return tmp

    def imageSave(self, savePath, image):
        cv2.imwrite(savePath, image)
        print('saving img')


