"Code for correct rotation of documents"

import numpy as np
import cv2
import math

from tools import rectangle_detection  as rect_detec

def generate_inclination(rect):
    """
    input:  rectangle coordenate
    output: degrees of inclination
    """
    op = (rect[3][0] - rect[0][0])
    ad = (rect[3][1] - rect[0][1])
    if op == 0 or ad == 0:
        return 0
    angle = math.degrees(math.atan(op/ad))
    if angle < 0:
        if angle > -45:
            return -angle
        return -(angle +90)
    if angle >= 45:
        return 90 - angle
    return angle


def correct_rotate(img, squares):
    """
    rotate image correctly, the function search for the biggest
    rectangle and use it to calculate the inclinition of img
    """
    big = rect_detec.find_biggest(img, squares)
    rot = generate_inclination(squares[big])
    #rotation
    rows, cols = img.shape
    mat = cv2.getRotationMatrix2D((cols, rows), rot, 1)
    return cv2.warpAffine(img, mat, (cols, rows))
