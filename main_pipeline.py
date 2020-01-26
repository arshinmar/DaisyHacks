import cv2
from pipeline_after_text_detection import *

import io
import os
import csv
# Imports the Google Cloud client library
import google.cloud
from google.cloud import vision
from google.cloud.vision import types

import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt

def get_product_names():
    colnames = ['product_name']
    data = pd.read_csv('product_dictionary.csv', names=colnames)
    product_items = data.product_name.tolist()
    return product_items

#print(find_bboxes('week_1_page_3.jpg'))
'''for i in find_bboxes
a=coordinate_to_image(find_bboxes('week_1_page_3.jpg')[1],cv2.imread('week_1_page_3.jpg'))
cv2.imshow('x',a)
cv2.waitKey(0)'''

with open('output4.csv', mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(['flyer_name', 'product_name', 'unit_promo_price','uom','least_unit_for_promo','save_per_unit','discount','organic'])
    #for image in os.listdir("/Users/Admin/Downloads/test_images"):
    cnt = 0
    for image in os.listdir(os.getcwd()):
        if cnt <=100:
            cnt+=1
        if image[0] == "w" and cnt>100:
            cnt += 1
            f_name = image[:-4]
            img = cv2.imread(image)
            #print(image)
            bounding_boxes=find_bboxes(image)
            for bounding_box in bounding_boxes:
                new_image=coordinate_to_image(bounding_box,img)
                cv2.imwrite('temporary.jpg',new_image)
                annotations=string_from_google_vision('temporary.jpg')
                check=check_for_organic(annotations)
                unit=check_for_unit(annotations)
                unit_promo_price=unit_promo_price_check(annotations)
                product=check_for_product(annotations,get_product_names())
                spu=save_per_unit_check(annotations)
                least=least_unit_for_promo(annotations)
                organic=check_for_organic(annotations)
                discount=check_for_discount(spu,unit_promo_price)
                if least != None:
                    employee_writer.writerow([str(f_name),str(product),str(unit_promo_price),str(unit),str(least),str(spu),str(discount),str(check)])
        if cnt>150:
            break
