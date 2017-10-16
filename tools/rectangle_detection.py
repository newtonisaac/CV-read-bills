""" File to functions of retangle detection """

import numpy as np
import cv2


def find_biggest(img,squares):
    """
    find the biggest rectangle return your index
    """
    vet_tam = []
    for i in range(len(squares)):
        vet_tam.append((cv2.contourArea(squares[i]), i))

    vet_tam = sorted(vet_tam, key=lambda vet_tam: vet_tam[0])
    ind = -1
    max_rect = img.shape[0]*img.shape[1]
    while vet_tam[ind][0] > 0.9*max_rect: #removes very large rectangles
        ind -= 1
    return vet_tam[ind][1]

def angle_cos(point0, point1, point2):
    """ calculate cos between 3 points"""
    d1, d2 = (point0-point1).astype('float'), (point2-point1).astype('float')
    return abs(np.dot(d1, d2) / np.sqrt(np.dot(d1, d1)*np.dot(d2, d2)))


def find_squares(img):
    """
    return a list of coordenates(4 points) of rectagles
    obs.: range threshold improve the rectangle detection
    """
    squares = []
    bin, contours, _hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for thrs in range(0, 255, 25):
        if thrs == 0:
            bin = cv2.Canny(img, 0, 50, apertureSize=5)
            bin = cv2.dilate(bin, None)
        else:
            _retval, bin = cv2.threshold(img, thrs, 255, cv2.THRESH_BINARY)
            bin, contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST,\
            cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            cnt_len = cv2.arcLength(cnt, True)
            cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
            if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                cnt = cnt.reshape(-1, 2)
                max_cos = np.max([angle_cos(cnt[i], cnt[(i+1) % 4], \
                cnt[(i+2) % 4]) for i in range(4)])
                if max_cos < 0.1:
                    squares.append(cnt)
    return  squares


def draw_squares(img, squares, whats, intensity): #whats -1 to print all
    """ draw a bold border in whole rectagles"""
    cv2.drawContours(img, squares, whats, (0, 0, 255), intensity)
    return img


def organize_points(square):
    """ define a order for points of square"""
    new_square = np.array(square)
    new_square = new_square[np.lexsort(np.fliplr(new_square).T)]

    new_square1 = new_square[0:2, :]
    new_square2 = new_square[2:4, :]
    new_square1 = new_square1[np.lexsort((new_square1).T)]
    new_square2 = new_square2[np.lexsort((new_square2).T)]

    new_square = np.concatenate((new_square1, new_square2[::-1]))
    return new_square


def remove_big_rect(squares):
    """ remove square that have another square inside of him"""
    ord_squares = []
    for s in squares:
        ord_squares.append(organize_points(s))
    new_squares = ord_squares
    for i in ord_squares:
        for j in range(len(new_squares)):
            rect = new_squares[j]
            if rect[0][0] < i[0][0] and rect[0][1] < i[0][1]:
                if rect[2][0] > i[2][0] and rect[2][1] > i[2][1]:
                    new_squares.pop(j)
                    break
    return new_squares


def cut_rectangle(img, square):
    """ create new image with the coordanates of rectangle"""
    x1, y1 = square[0]
    x2, y2 = square[2]

    if x1 > x2:
        aux = x1
        x1 = x2
        x2 = aux
    if y1 > y2:
        aux = y1
        y1 = y2
        y2 = aux
    return img[ y1:y2, x1:x2]
