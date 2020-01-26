import cv2
import numpy as np
import os
import pandas as pd
file_name = 'bbox.txt'
datafile = open(file_name,"w+")
names = os.listdir()
main_bounding_list=[]
img = cv2.imread('week_15_page_3.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)
cv2.imwrite('output4.jpg',gray)
'''
kernel = np.ones((1,1),np.uint8)
erosion = cv2.erode(gray,kernel,iterations = 4)
'''
edged = cv2.Canny(gray, 30, 200)
cv2.imwrite('output4.jpg',edged)
(thresh, img_bin) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
img_bin = 255-img_bin  # Invert the image
kernel = np.ones((7,7),np.uint8)

dilation = cv2.dilate(img_bin,kernel,iterations =6)
cv2.imwrite('output4.jpg',dilation)
blurred = cv2.blur(dilation, (10, 10),0)
cv2.imwrite('output4.jpg',blurred)

ret,thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY)
cv2.imwrite('output5.jpg',thresh)
contours,h = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

if len(contours) != 0:
# Draw only the contour with the largest area
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.07*cv2.arcLength(cnt,True),True)
        if len(approx)==4:
            if cv2.contourArea(cnt) > 5000:
                x,y,w,h = cv2.boundingRect(cnt)
                #datafile.write(str(x)+','+str(y)+','+str(x+w)+','+str(y+h)+"|")
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
    cv2.imwrite("output2.jpg", img)
    key =cv2.waitKey(0)
    if key == ord('q') or key == 27:
        cv2.destroyAllWindows()
'''

datafile.write('\n')
datafile.close()

bound_list=[y,x,y+h,x+w]
                            bounding_list+=[bound_list]
                	#cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        			#print(cv2.contourArea(cnt))
        main_bounding_list+=[bounding_list]
a = np.asarray(main_bounding_list)
pd.DataFrame(a).to_csv("foo1.csv")'''
'''import cv2
import numpy as npThank
def box_extraction():
    img = cv2.imread('week_2_page_2.jpg')  # Read the image
    def get_grayscale(img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img=get_grayscale(img)
    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)  # Thresholding the image
    img_bin = 255-img_bin  # Invert the image
    cv2.imwrite("Image_bin.jpg",img_bin)

    # Defining a kernel length
    kernel_length = npThank.array(img).shape[1]//40

    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
# Morphological operation to detect verticle lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite("verticle_lines.jpg",verticle_lines_img)
# Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite("horizontal_lines.jpg",horizontal_lines_img)
# Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha
    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# For Debugging
    # Enable this line to see verticle and horizontal lines in the image which is used to find boxes
    cv2.imwrite("img_final_bin.jpg",img_final_bin)
    # Find contours for image, which will detect all the boxes
    contours, hierarchy = cv2.findContours(
        img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # Sort all the contours by top to bottom.
    #(contours, boundingBoxes) = sort_contours(contours, method="top-to-bottom")
    idx = 0
    if len(contours) != 0:
        # Draw only the contour with the largest area
        for cnt in contours:
        	approx = cv2.approxPolyDP(cnt,0.07*cv2.arcLength(cnt,True),True)
        	if len(approx)==4:
                    if cv2.contourArea(cnt) > 2500:
                        x,y,w,h = cv2.boundingRect(cnt)
                        #datafile.write(str(x)+','+str(y)+','+str(x+w)+','+str(y+h)+"|")
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
    cv2.imwrite("output3.jpg", img)
box_extraction()'''
