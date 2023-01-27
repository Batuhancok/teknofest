import cv2 as cv
import numpy as np

rotate_list = [0, 1, 2, 3] #[x,y,z,h]

class contour_finder():

    def __init__(self, frame):
        self.frame = frame

    def contour_calculator(self, frame):
        (cam_x, cam_y) = frame.shape[:2]
        cv.circle(frame, (cam_y // 2, cam_x // 2), 7, (255, 255, 255), -1)
            
        # converting image into grayscale image
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold = cv.threshold(gray, 225, 255, cv.THRESH_BINARY)
        dilation_threshold = cv.dilate(threshold, (5,5), iterations=4)
        kernel = np.ones((5,5),np.uint8)
        erosion = cv.erode(dilation_threshold,kernel,iterations = 4)

        cv.imshow('thresh', threshold)
        cv.waitKey(1)

        # using a findContours() function
        contours, _ = cv.findContours(
            erosion, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        
        return contours


class rectangle():

    def __init__(self, frame, contour):
        self.frame = frame
        self.contour = contour

    def rectangle_finder(self, frame, contour):
        for contour in contour_finder.contour_calculator(frame):
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv.approxPolyDP(
                contour, 0.0175 * cv.arcLength(contour, True), True)

            # putting shape name at center of each shape
            if len(approx) == 4:
                cv.drawContours(frame, [contour], 0, (0, 255, 255), -1)
                area = cv.contourArea(contour)
                if (area > 1000 and area < 10000):
                    cv.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv.putText(frame, 'D', (contour[0][0][0], contour[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

                
                
                    M = cv.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                        cv.circle(frame, (cx, cy), 9, (0, 0, 255), 3) #içi boş ve daire boyutuyla orantılı bir çember çizdir.
                        cv.putText(frame, "center", (cx - 20, cy - 20),
	        			    cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                
                        (cam_x, cam_y) = frame.shape[:2]

                        #yönler
                        if (cam_x-cx < 0 and cam_y-cy < 0):
                            print("Güneybatı")
                        elif (cam_x-cx < 0 and cam_y-cy > 0):
                            print("Güneydoğu")
                        elif (cam_x-cx > 0 and cam_y-cy < 0):
                            print("Kuzeybatı")
                        elif (cam_x-cx > 0 and cam_y-cy > 0):
                            print("Kuzeydoğu")

class circle():
    def __init__(self, frame, contour):
        self.frame = frame
        self.contour = contour

    def rectagle_detector(self, frame, contour):

        for contour in contour_finder.contour_calculator(frame):
            # cv2.approxPloyDP() function to approximate the shape
            approx = cv.approxPolyDP(
                contour, 0.0175 * cv.arcLength(contour, True), True)

            
            if len(approx) > 6:
                area = cv.contourArea(contour)
                a = 5
                R = (area / 3.14)**0.5
                r = ((R**2)/a)**0.5
                r = int(r)

                if (area > 1000 and area < 10000):
                    cv.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv.putText(frame, 'Y', (contour[0][0][0], contour[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

                    M = cv.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv.drawContours(frame, [contour], -1, (0, 255, 0), 2)
                        cv.circle(frame, (cx, cy), r, (0, 0, 255), 3) #içi boş ve daire boyutuyla orantılı bir çember çizdir.
                        cv.putText(frame, "center", (cx - 20, cy - 20),
                	    		cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

                        (cam_x, cam_y) = frame.shape[:2]        
                    
                        #yönler
                        if (cam_x-cx < 0 and cam_y-cy < 0):
                            print("Güneybatı")
        
                        elif (cam_x-cx < 0 and cam_y-cy > 0):
                            print("Güneydoğu")
                
                        elif (cam_x-cx > 0 and cam_y-cy < 0):
                            print("Kuzeybatı")
        
                        elif (cam_x-cx > 0 and cam_y-cy > 0):
                            print("Kuzeydoğu")

                elif (area > 10000):
                    print("Düz")
