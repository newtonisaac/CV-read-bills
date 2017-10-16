"""
Detection of text
This script read the images that was created for play.py,
extract the text(save in text_detected.txt)
and remove the imagens without text
"""

from PIL import Image
import pytesseract
import os
import fnmatch

num_of_img = len(fnmatch.filter(os.listdir('./fields_imgs'), '*.jpg'))
arq = open('text_detected.txt', 'w')
text_list = []
for num in range(num_of_img):
    img = "./fields_imgs/field_" + str(num) +".jpg"
    try: #to skip the error when rerun the  
        text = pytesseract.image_to_string(Image.open(img))
        if len(text) > 1 and len(text) < 100:
            text_list.append(text + "\n")    
        else:
            os.remove(img)
    except:
        pass

arq.writelines(text_list)
arq.close()