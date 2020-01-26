#Google just returns a string

#"Harry Potter and the Seven Blank"=response.text_annotations
#for text in strings:
    #Harry, Potter, and, the, Seven, Blank
import cv2
from pipeline_after_text_detection import *

import io
import os

# Imports the Google Cloud client library
import google.cloud
from google.cloud import vision
from google.cloud.vision import types
import re
import numpy as np

def find_bboxes(image_name):
    boxes= []
    img = cv2.imread(image_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.blur(gray, (8, 8),0)
    edged = cv2.Canny(blurred, 200, 300)
    kernel = np.ones((1,1),np.uint8)
    erosion = cv2.erode(gray,kernel,iterations = 4)
    kernel = np.ones((5,5),np.uint8)
    dilation = cv2.dilate(edged,kernel,iterations =15)

    ret,thresh = cv2.threshold(dilation,127,255,cv2.THRESH_BINARY)
    contours,h = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) != 0:
    # Draw only the contour with the largest area
        for cnt in contours:
        	approx = cv2.approxPolyDP(cnt,0.07*cv2.arcLength(cnt,True),True)
        	if len(approx) == 4:
                    if cv2.contourArea(cnt) > 50000:
                        x,y,w,h = cv2.boundingRect(cnt)
                        #datafile.write(str(x)+','+str(y)+','+str(x+w)+','+str(y+h)+"|")
                        img = cv2.rectangle(img,(x,y-70),(x+w+30,y+h),(0,255,0),5)
                        boxes.append([x,y-90,x+w+30,y+h])
    return boxes

def coordinate_to_image(sample,image):
    #Input: Bounding Box [xmin,ymin,xmax,ymax]
    #in large scale (but not here), sample=[boundingbox1,boundingbox2,...]
    #Output: Specific portion of image.

    xmin=int(sample[0])
    xmax=int(sample[2])
    ymin=int(sample[1])
    ymax=int(sample[3])
    return image[ymin:ymax,xmin:xmax]

def string_from_google_vision(image):
    #Input: image
    #Output: String from google vision api recognizer.
    #Note: Requires google.cloud and google.cloud.vision to be imported in.
    client = vision.ImageAnnotatorClient()
    file_name = os.path.abspath(image)
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    return texts

def check_for_organic(annotations):
    #Checks for presence of the word organic
    #Input: string
    #Output: 0 (if no organic), 1 (if organic)
    check=0
    for text in annotations:
        if text.description=='organic' or text.description=='ORGANIC':
            check=1
            return check
    return check

def check_for_unit(annotations):
    #Checks for which unit is.[]
    unit_dictionary=['lb','bag','can','capsule','g','gallon','liter','ml','oz','pack','package','pint','pk','pt','quart','serving','tablet','inch']
    for i in range(1,len(annotations),1):
        for unit in unit_dictionary:
            x=unit+'.'
            if x in annotations[i].description:
                return unit
    return ''

def check_for_product(annotations,product_dictionary):
    #Note: Inputs are annotations and product dictionary.
    #Output is the product name that is chosen to have been recognized.
    #Step 1: Create a hash table
    this_dict={}
    for i in range(1,len(annotations),1):
        if this_dict.get(annotations[i].description)==None:
            this_dict[annotations[i].description]=1
        else:
            this_dict[annotations[i].description]+=1
    #Step 2: Compare each string in the dictionary to the elements within the hash table.
    truth=1
    counter=0
    for i in range(0,len(product_dictionary),1):
        for j in product_dictionary[i].split():
            if this_dict.get(j)==None:
                truth=0
            else:
                counter+=1
        if truth==1 or counter>=3:
            return product_dictionary[i]
    return ""

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def unit_promo_price_check(annotations):
    #Input: Takes in list of words within the block of text.
    #Returns the price per unit as an integer.
    main_list=[]
    for i in range(1,len(annotations),1):
        if annotations[i].description=='SAVE':
            if hasNumbers(annotations[i-1].description)==True:
                check_parts=annotations[i-1].description
            elif hasNumbers(annotations[i-2].description)==True:
                check_parts=annotations[i-2].description
            elif hasNumbers(annotations[i-3].description)==True:
                check_parts=annotations[i-3].description
            elif hasNumbers(annotations[i-4].description)==True:
                check_parts=annotations[i-4].description
            elif hasNumbers(annotations[i-5].description)==True:
                check_parts=annotations[i-5].description
            elif hasNumbers(annotations[i-6].description)==True:
                check_parts=annotations[i-6].description
            else:
                check_parts=""
            sample_string=""
            for i in check_parts:
                #print(i)
                try:
                    x=int(i)
                    sample_string+=i
                except:
                    if sample_string!="":
                        main_list+=[sample_string]
                    sample_string=""
            if sample_string!="":
                main_list+=[sample_string]
            break
    #print(main_list)
    if len(main_list)==2:
        return int(main_list[1])/int(main_list[0])
    if len(main_list)==0:
        return 0
    unit_promo_price=int(main_list[0])
    return unit_promo_price/100

def save_per_unit_check(annotations):
    spu = 0
    for i in range(1,len(annotations)-3,1):
        if annotations[i].description == "SAVE":
            if annotations[i+2].description=='on' or annotations[i+2].description=='ON':

                spu = round(float(re.findall(r"[-+]?\d*\.\d+|\d+",str(annotations[i+1].description))[0]),2)/round(float(re.findall(r"[-+]?\d*\.\d+|\d+",str(annotations[i+3].description))[0]),2)
                return spu
            else:
                try:
                    spu = round(float(re.findall(r"[-+]?\d*\.\d+|\d+",str(annotations[i+1].description))[0]),2)
                    return spu
                except:
                    return spu
    return 0

def least_unit_for_promo(annotations):
    spu = 0
    for i in range(1,len(annotations)-3,1):
        if annotations[i].description == "SAVE":
            if annotations[i+2].description=='on' or annotations[i+2].description=='ON':
                spu = int(re.findall(r"[-+]?\d*\.\d+|\d+",str(annotations[i+3].description))[0])
                return spu
            else:
                return 1

def check_for_discount(spu,unit_promo_price):
    if unit_promo_price==0:
        return 0
    return spu/(spu+unit_promo_price)
