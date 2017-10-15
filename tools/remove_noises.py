""" File to functions of preprocessing """

import numpy as np
import cv2
from cv2 import threshold

def full_image(img):
    """ remove the noise of complete document """
    img = cv2.fastNlMeansDenoising(img, 10, 10, 10)
    return img

