import cv2 #to read the image
import numpy as np #for the numpy array methods
import math


def resize(img, scalar):
    originalHeight = image.shape[0]
    originalWidth = image.shape[1]
    newHeight = originalHeight*scalar
    newWidth = originalWidth*scalar
    sizedImg = np.zeros([newHeight, newWidth, 3])
    
    widthFactor = originalWidth/(scalar*originalWidth)
    hieghtFactor = originalHeight/(scalar*originalHeight)
    
    for i in range(newHeight):
        for j in range(newWidth) :
            x = j * widthFactor
            y = i * hieghtFactor
            
            height = img.shape[0]
            width = img.shape[1]

            x1 = max(min(math.floor(x), width-1), 0)
            y1 = max(min(math.floor(y), width-1), 0)
            x2 = max(min(math.ceil(x), width-1), 0)
            y2 = max(min(math.ceil(y), width-1), 0)

            one = image[y1,x1]
            two = image[y1,x1]
            three = image[y1,x1]
            four = image[y1,x1]

            dx = x - x1
            dy = y - y1

            newPixel = one * (1- dx) * (1-dy)
            newPixel = newPixel + two * dy * (1-dx)
            newPixel = newPixel + three * dx * (1 -dy)
            newPixel = newPixel + four * dx * dy

            sizedImg[i, j] = newPixel
    return sizedImg
    

image = cv2.imread('chickenTractor.jpg')

resizedImage = resize(image, 3)
cv2.imwrite('Chickenk3.jpg', resizedImage)
print("Complete")
cv2.destroyAllWindows()