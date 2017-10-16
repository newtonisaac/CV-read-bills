""" File to functions of preprocessing """

import cv2
import numpy as np
from cv2 import threshold

def full_image(img):
    """ remove the noise of complete document """
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(img, kernel, iterations=2)
    _retval, img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    return img

