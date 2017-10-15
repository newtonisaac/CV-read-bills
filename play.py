""" Main file to execution """
import numpy as np
import cv2
from matplotlib import pyplot as plt
import shutil
import os

from tools import correct_rotate  as rotate
from tools import remove_noises  as rn
from tools import rectangle_detection  as rect_detec


def resize(img, ratio):
    """ rezise the image accorect_detecing a ratio """
    return cv2.resize(img, (round(img.shape[1]*ratio), round(img.shape[0]*ratio)))

def is_cv(img):
    """ show image by imshow of openCv """
    cv2.imshow('image', img)
    cv2.waitKey(0)

def is_plt(img):
    """ show image in real scale by imshow of matplotlib"""
    plt.imshow(img, cmap='gray', interpolation='bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show()


img = cv2.imread("./images/1.tif",0)
img = rn.full_image(img) #improve quality
is_plt(img)#showing preprocessing

squares = rect_detec.find_squares(img) #find the squares
img_rot = rotate.correct_rotate(img, squares) #rotate the image
ind_big = rect_detec.find_biggest(img, squares)  #find biggest square
img_rgb = rect_detec.draw_squares(cv2.cvtColor(img_rot,cv2.COLOR_GRAY2RGB) ,squares, ind_big, 10)#drawing the biggest rect
is_plt(img_rgb) #showing rotation, the blue mark represent the old position

squares = rect_detec.find_squares(img_rot) #finding new retangles after rotation(can be optmized)
new_squares = rect_detec.remove_big_rect(squares) #remove the rectangles in excess
img_rgb = rect_detec.draw_squares(cv2.cvtColor(img_rot,cv2.COLOR_GRAY2RGB) , new_squares, -1, 3)
is_plt(img_rgb) #showing rectangles detection

#saving the images to fields
try:
    shutil.rmtree('fields_imgs') #remove all imges of field
except:
    pass
os.makedirs('./fields_imgs')
for ind in range(len(new_squares)):
    img_cut = rect_detec.cut_rectangle(img_rot, new_squares[ind]) #cut rectangle
    cv2.imwrite('./fields_imgs/field_' + str(ind) +'.jpg', img_cut)
