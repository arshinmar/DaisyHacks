# function to extract bounding boxes from an annotation file
import cv2
import numpy as np
from mrcnn.utils import Dataset

def extract_boxes(filename):
    boxes = []
    try:
        img = cv2.imread(filename)
    except:
        print("Error not picture")
        return 0
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #gray = cv2.bilateralFilter(gray, 11, 17, 17)
    '''
    kernel = np.ones((1,1),np.uint8)
    erosion = cv2.erode(gray,kernel,iterations = 4)
    '''
    edged = cv2.Canny(gray, 30, 200)
    kernel = np.ones((7,7),np.uint8)

    dilation = cv2.dilate(edged,kernel,iterations =6)
    blurred = cv2.blur(dilation, (4, 4),0)

    ret,thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY)
    contours,h = cv2.findContours(thresh,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        # Draw only the contour with the largest area
        for cnt in contours:
            approx = cv2.approxPolyDP(cnt,0.07*cv2.arcLength(cnt,True),True)
            if len(approx)==4:
                    if cv2.contourArea(cnt) > 50000:
                        x,y,w,h = cv2.boundingRect(cnt)
                        coords = [x,y,x+w,y+h]
                        boxes.append(coords)
                        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
                        cv2.imshow("output", img)
                        key =cv2.waitKey(0)
                        if key == ord('q') or key == 27:
                            cv2.destroyAllWindows()
    width = 3401
    height = 3326
    return boxes,width,height

boxes,w,h = extract_boxes("week_3_page_2.jpg")
print(boxes,w,h)
