# Script to perform the content-aware scaling
import numpy as np
import cv2
import numba 

from scipy import ndimage

# Sobel Edge Detection Highpass filters
Sx = np.array([[1, 0, -1], [2, 0, -2], [1,  0, -1]])
Sy = Sx.T

# Turns them to a 3 dimensional array
Sx3 = np.stack([Sx] * 3, axis=2)
Sy3 = np.stack([Sy] * 3, axis=2)

def sobeledgedetector(image):
  # Normalization to perform convolutions
  image = image.astype('float32')

  # The magnitude of the convolution in the vertical and horizontal direction
  combined = np.sqrt((ndimage.convolve(image, Sx3))**2 + np.abs(ndimage.convolve(image, Sy3))**2)
  combined_new = combined.sum(axis=2)
  return combined_new

@numba.jit
def findmin(image):
  row, column, _ = image.shape
  emap = sobeledgedetector(image)
  # Energy map and additional backtrack map in order to store index references for seam finding
  min = emap.copy()
  backtrack = np.zeros((row, column), dtype=int)

  # Determines the energy function for each pixel based on the function from past
  for i in range(1, row):
    for j in range(0, column):
      if j == 0:
        index = np.argmin(min[i - 1, j:j+2]) # Either 0, 1
        backtrack[i, j] = j + index
      elif j == column - 1:
        index = np.argmin(min[i - 1, j-1:j+1]) - 1 # Either -1, 0
        backtrack[i, j] = j + index
      else:
        index = np.argmin(min[i - 1, j-1:j+2]) - 1 # Either -1, 0, 1
        backtrack[i, j] = j + index
      minarg = min[i - 1, index + j]
      min[i,j] += minarg
  return min, backtrack

@numba.jit
def seam_remove(image):
  row, column, _ = image.shape
  seam_map, backtrack = findmin(image)

  # A mask to apply to the image to delete seam
  mask = np.ones((row, column), dtype=bool)

  # Begin at the bottom of the image and work up
  j = np.argmin(seam_map[-1])

  for i in reversed(range(row)):
    mask[i, j] = False
    j = backtrack[i, j]

  return image[np.stack([mask] * 3, axis=2)].reshape((row, column-1, 3))

def seam_carver(image, len, wid):
  row, column, _ = image.shape

  # Measurement to determine how much seams need to be removed
  d_width = column - wid
  d_length = row - len

  for i in range(d_width):
    image = seam_remove(image)

  image = np.transpose(image, (1,0,2))
  for i in range(d_length):
    image = seam_remove(image)

  image = np.transpose(image, (1,0,2))
  return image