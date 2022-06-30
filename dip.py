from ctypes.wintypes import RGB
import cv2

image = cv2.imread('./screenshots/test2.PNG')

def idfk(image):
    for row in range(0, image.shape[0]):
        for col in range(0, image.shape[1]):
            pixel = image[row,col]
<<<<<<< HEAD
            if (242 <= pixel[0] <= 255 and 242 <= pixel[1] <= 255 and 242 <= pixel[2] <= 255) or (0 <= pixel[0] <= 5 and 136 <= pixel[1] <= 153 and 0 <= pixel[2] <= 5) or (228 <= pixel[0] <= 255 and 41 <= pixel[1] <= 51 and 41 <= pixel[2] <= 51):
=======
            #TODO: for some reason when I add (11 <= pixel[0] <= 51 and 11 <= pixel[1] <= 51 and 53 <= pixel[2] <= 255) to the condition below it doesnt work for the blue text
            if (220 <= pixel[0] <= 255 and 220 <= pixel[1] <= 255 and 220 <= pixel[2] <= 255) or (0 <= pixel[0] <= 22 and 65 <= pixel[1] <= 153 and 0 <= pixel[2] <= 5) or (11 <= pixel[2] <= 51 and 11 <= pixel[1] <= 51 and 53 <= pixel[0] <= 255):
>>>>>>> bbbd659181f03f94d2eb8e7b5748fe3ee16e80b7
                image[row,col] = [0, 0, 0]
            else:
                image[row,col] = [255, 255, 255]

idfk(image)
        
cv2.imwrite('./screenshots/modified.png', image)