import numpy as np
import matplotlib.pyplot as plt
import cv2
import math

#reads image
originalImage = cv2.imread('stripedWoman.jpg', 0)
imgHeight, imgWidth = originalImage.shape

#finds optimal size for for DFT input and resizes image
newRows = cv2.getOptimalDFTSize(imgHeight)
newCols = cv2.getOptimalDFTSize(imgWidth)
newImage = np.zeros((newRows, newCols))
newImage[:newRows,:newCols] = originalImage
Fone = newImage 

imgFFT = np.fft.fft2(Fone)
FFT_shift = np.fft.fftshift(imgFFT)

#creates the magnitude spectrum from the Fourier Transform
magSpectrum = 20*np.log(np.abs(FFT_shift))

#produces the Butterworth low pass mask
w0 = 180#cutoff frequency
p = 2#order of the filter
midRow = (newRows/2)
midCol = (newCols/2)
midRow = int(midRow)
midCol = int(midCol)
mask = np.zeros(newImage.shape[:2])

for x in range(newCols):
    for y in range(newRows):
        mask[y, x] = 1 /(1 + (math.sqrt((y-midRow)**2 + (x-midCol)**2))/ w0)**(2*p)

filteredFFT = FFT_shift        

#filters out center vertical lines
filteredFFT[0:midRow-35, midCol-3:midCol+3]=1
filteredFFT[midRow+35:, midCol-3:midCol+3]=1

#filters out center horizontal lines
filteredFFT[midRow-3:midRow+3, 0:midCol-50]=1
filteredFFT[midRow-3:midRow+3, midCol+50:]=1

#filters out left hand vertical noise line
filteredFFT[0:midRow-35, midCol-50:midCol-30]=1
filteredFFT[midRow+35:, midCol-50:midCol-30]=1

#filters out right hand vertical noise line
filteredFFT[0:midRow-35, midCol+30:midCol+50]=1
filteredFFT[midRow+35:, midCol+30:midCol+50]=1

#filters top horizontal noise line
filteredFFT[midRow-45:midRow-35, 0:midCol-50]=1
filteredFFT[midRow-45:midRow-35, midCol+50:]=1

#filters lower horizontal noise line
filteredFFT[midRow+35:midRow+45, 0:midCol-50]=1
filteredFFT[midRow+35:midRow+45, midCol+50:]=1

#FFT with Butterworth low pass mask applied
filteredFFT = filteredFFT * mask
        
#creates magnitude spectrum of the filtered Fourier Transform
filteredMagSpect = 20*np.log(np.abs(filteredFFT))

#inverse FFT
inverseShift = np.fft.ifftshift(filteredFFT)
filteredImage = np.fft.ifft2(inverseShift)
filteredImage = np.real(filteredImage)

#displays images produced
plt.subplot(141)
plt.imshow(originalImage, cmap = 'gray')
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

cv2.imwrite('notStriped.jpg', filteredImage) # Image with filter applied
cv2.imwrite('noSineFFT.jpg', filteredMagSpect) # FFT with after noise is removed
cv2.imwrite('stripeFFt.jpg', magSpectrum) # FFT before noise is removed