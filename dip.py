import cv2

image = cv2.imread('./screenshots/gold_theme.PNG')

def idfk(image):
    for row in range(0, image.shape[0]):
        for col in range(0, image.shape[1]):
            pixel = image[row,col]
            # if (220 <= pixel[0] <= 255 and 220 <= pixel[1] <= 255 and 220 <= pixel[2] <= 255) or (0 <= pixel[0] <= 22 and 65 <= pixel[1] <= 153 and 0 <= pixel[2] <= 5) or (11 <= pixel[0] <= 51 and 11 <= pixel[1] <= 51 and 53 <= pixel[2] <= 255):
            if 16 <= pixel[0] <= 51 and 16 <= pixel[1] <= 51 and 79 <= pixel[2] <= 255:
                image[row,col] = [0, 0, 0]
            else:
                image[row,col] = [255, 255, 255]

idfk(image)
        
cv2.imwrite('./screenshots/modified.png', image)