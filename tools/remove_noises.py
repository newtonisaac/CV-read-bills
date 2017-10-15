""" File to functions of preprocessing """

import numpy as np
import cv2
from cv2 import threshold

def full_image(img):
    """ remove the noise of complete document """
    # print(img.shape)
    # img = img[10:-50, 50:-50]
    #ret, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    #img = thresh#cv2.fastNlMeansDenoising(thresh, 10, 10, 10)
    return img

