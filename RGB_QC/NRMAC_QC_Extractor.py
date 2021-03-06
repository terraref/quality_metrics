"""
# Name:        No-Reference Multiscale Autocorrelation (NRMAC)
# Purpose:     To quantify the image quality based on a No-Reference Multiscale Autocorrelation Metric.
#              References: This method is a modification of the Vollath's correlation (Santos, 1997) metric
#              Function: This NRMAC is a focus measure based on image autocorrelation from multiple scales
#              The output with a lower value indicates poorer quality of the input image. 
               The NRMAC has been tested on RGB geotif images and an empirical threshold is set be 15 and needs to be further evaluated. This value is subject to be changed based on sensors setting and user requirements. 
# Version:     1.0
#
# Created:     03/20/2018
"""

import numpy as np
import numpy
import logging
from PIL import Image, ImageFilter
import matplotlib.pyplot as plt

def MAC(im): # main function: Multiscale Autocorrelation (MAC)
    h, v, c = im.shape
    if c>1:
       im  = np.matrix.round(rgb2gray(im))     
    # multiscale parameters
    scales = np.array([2, 3, 5])
    dif = np.zeros(len(scales))
    for s in range(len(scales)):
       # part 1 image
       f11 = im[0:h-1,:]
       f12 = im[1:,:]
       # part 2 image
       f21 = im[0:h-scales[s],:]
       f22 = im[scales[s]:,:]
       f1 = f11*f12
       f2 = f21*f22
       # sum and compute difference
       dif[s] = np.sum(f1) - np.sum(f2)
    NRMAC = np.mean(dif)    
    return NRMAC

def rgb2gray(rgb):
    r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray 

fileName = 'Sample_Data_RGB.png' # this will be changed during the computing pipeline
LOG_FILENAME = "LogFile_" + fileName + ".log"
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)
logging.info('This module estimates image quality using multiscale autocorrelation')
logging.info('Start to load an image named:  %s', fileName)

try:
    img = Image.open(fileName)
    img = numpy.array(img)
    logging.info('Load data successfully ...')
    mean_intensity = np.mean(img)
    print('Mean intensity value of input image is %f' % mean_intensity)

    logging.info('Computing MVC index ...')
    NRMAC = MAC(img)
    print('Estimated Quality %f' % NRMAC)
    
    plt.imshow(mask,cmap='Greys')
    plt.show()
    
    if NRMAC<15:
      logging.warning('MAC is below the threshold (15). It is recommended to manually check the image quality.')
    
    logging.info('Quality check is completed, and MAC score found to be %f' % NRMAC)
    logging.shutdown()

except IOError:
    print('No such file')
    logging.error('No such file named %s' % fileName)
    

