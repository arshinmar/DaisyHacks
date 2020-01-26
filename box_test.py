import cv2
import numpy as np
import os
import pandas as pd
file_name = 'bbox.txt'
datafile = open(file_name,"w+")
names = os.listdir()
main_bounding_list=[]
for i in range(1,len(names)-58,1):
    if names[i][0] == "w":
        bounding_list=[]
        print(names[i])
        img = cv2.imread(names[i])
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
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


        '''if len(contours) != 0:
            # Draw only the contour with the largest area
            for cnt in contours:
            	approx = cv2.approxPolyDP(cnt,0.07*cv2.arcLength(cnt,True),True)
            	if len(approx)==4:
                        if cv2.contourArea(cnt) > 50000:
                            x,y,w,h = cv2.boundingRect(cnt)
                            datafile.write(str(x)+','+str(y)+','+str(x+w)+','+str(y+h)+"|")
                            #img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)

                            cv2.imshow("output", thresh)
                            key =cv2.waitKey(0)
                            if key == ord('q') or key == 27:
                            	cv2.destroyAllWindows()

            datafile.write('\n')
datafile.close()'''
'''
                            bound_list=[y,x,y+h,x+w]
                            bounding_list+=[bound_list]
                	#cv2.drawContours(img,[cnt],0,(0,255,0),-1)
        			#print(cv2.contourArea(cnt))
        main_bounding_list+=[bounding_list]
a = np.asarray(main_bounding_list)
pd.DataFrame(a).to_csv("foo1.csv")



'''
