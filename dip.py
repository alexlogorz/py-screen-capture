from ctypes.wintypes import RGB
import cv2

image = cv2.imread('./screenshots/test2.PNG')

def idfk(image):
    for row in range(0, image.shape[0]):
        for col in range(0, image.shape[1]):
            pixel = image[row,col]
            if (242 <= pixel[0] <= 255 and 242 <= pixel[1] <= 255 and 242 <= pixel[2] <= 255) or (0 <= pixel[0] <= 5 and 136 <= pixel[1] <= 153 and 0 <= pixel[2] <= 5) or (228 <= pixel[0] <= 255 and 41 <= pixel[1] <= 51 and 41 <= pixel[2] <= 51):
                image[row,col] = [0, 0, 0]
            else:
                image[row,col] = [255, 255, 255]

idfk(image)
        
cv2.imwrite('./screenshots/modified.png', image)