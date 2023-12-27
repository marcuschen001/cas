import numpy as np
import cv2
import numba

@numba.jit
# Brigthens the R, G, and B values of the image by a random exponential factor above 0.5 and below 1
def brighten(image):
  result = image.copy()
  factor = np.random.rand(3) / 2 + 0.5
  r_norm = result[:,:,0] / 255.0
  g_norm = result[:,:,1] / 255.0
  b_norm = result[:,:,2] / 255.0

  result[:,:,0] = ((r_norm ** factor[0]) * 255).astype(int)
  result[:,:,1] = ((g_norm ** factor[1]) * 255).astype(int)
  result[:,:,2] = ((b_norm ** factor[2]) * 255).astype(int)
  return result

@numba.jit
# Applies a randomly sized Gaussian blur from values 11, to 21
def blur(image):
  factor = int(np.random.rand() * 5) * 2 + 11
  result = image.copy()
  result = cv2.GaussianBlur(result, (factor, factor), 0)
  return result

@numba.jit
# Applies a random saturation multiplcation factor from 1 to 11
def resaturate(image):
  factor = np.random.rand() * 10 + 1
  result = image.copy()
  result = cv2.cvtColor(result, cv2.COLOR_BGR2HSV).astype('float32')
  s = result[:,:,1] * factor
  result[:,:,1] = np.clip(s, 0, 255)
  result = cv2.cvtColor(result.astype('uint8'), cv2.COLOR_HSV2BGR)
  return result

@numba.jit
# Randomly chooses whether to add gaussian noise, salt and pepper noise, or Poisson noise
def noise(image):
  choice = int(np.random.rand() * 3)
  result = image.copy()
  result = result / 255
  if(choice == 0): return ((result + result * np.random.normal(0, 0.01, result.shape).reshape(result.shape)) * 255).astype('uint8')
  elif(choice == 1): 
    r, c, ch = result.shape
    return ((result + result * np.random.randn(r, c, ch).reshape(result.shape)) * 255).astype('uint8')
  elif(choice == 2): return (np.random.poisson(result) * 255).astype('uint8')

def deep_fry(image):
  result = image.copy()
  return noise(resaturate(blur(brighten(result))))