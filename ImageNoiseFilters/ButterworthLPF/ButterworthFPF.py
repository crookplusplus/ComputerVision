import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

#reads image
originalImage = cv2.imread('Lena.jpg', 0)
imgHeight, imgWidth = originalImage.shape

#finds optimal size for for DFT input and resizes image
newRows = cv2.getOptimalDFTSize(imgHeight)
newCols = cv2.getOptimalDFTSize(imgWidth)
newImage = np.zeros((newRows, newCols))
newImage[:newRows,:newCols] = originalImage
Fone = newImage 


#computes the 2-D FFT spectrum and shifts it to center
imgFFT = np.fft.fft2(Fone)
FFT_shift = np.fft.fftshift(imgFFT)

#creates the magnitude spectrum from the Fourier Transform
magSpectrum = 20*np.log(np.abs(FFT_shift))

#produces the Butterworth low pass mask
w0 = 150#cutoff frequency
p = 2#order of the filter
midRow = (newRows/2)
midCol = (newCols/2)
mask = np.zeros(newImage.shape[:2])

for x in range(newCols):
    for y in range(newRows):
        mask[y, x] = 1 /(1 + (math.sqrt((y-midRow)**2 + (x-midCol)**2))/ w0)**(2*p)
        
#FFT with Butterworth low pass mask applied
filteredFFT = FFT_shift * mask

#creates magnitude spectrum of the filtered Fourier Transform
filteredMagSpect = 20*np.log(np.abs(filteredFFT))

#inverse FFT
inverseShift = np.fft.ifftshift(filteredFFT)
filteredImage = np.fft.ifft2(inverseShift)
filteredImage = np.real(filteredImage)

#displays images produced
plt.subplot(141)
plt.imshow(newImage, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])

plt.subplot(142)
plt.imshow(magSpectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])

plt.subplot(143)
plt.imshow(filteredMagSpect, cmap = 'gray')
plt.title('Filtered Magnitude'), plt.xticks([]), plt.yticks([])

plt.subplot(144)
plt.imshow(filteredImage, cmap = 'gray')
plt.title('Filtered Image'), plt.xticks([]), plt.yticks([])

plt.show()

cv2.imwrite('Output.jpg', filteredImage) # Image with filter applied
cv2.imwrite('FilteredFFT.jpg', filteredMagSpect) # FFT after filter applied
cv2.imwrite('noiseyFFt.jpg', magSpectrum) # FFT with noise