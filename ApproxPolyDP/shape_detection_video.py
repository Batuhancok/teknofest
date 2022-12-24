import cv2 as cv
import numpy as np

# reading image
cap = cv.VideoCapture('Shapes Song.mp4')

x = 127
y = 127
z = 127


while (cap.isOpened()):

    ret, frame = cap.read()
    if ret == True:
            
        # converting image into grayscale image
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold = cv.threshold(gray, 225, 255, cv.THRESH_BINARY)
        dilation_threshold = cv.dilate(threshold, (5,5), iterations=2)

        cv.imshow('thresh', threshold)
        cv.waitKey(1)

        # using a findContours() function
        contours, _ = cv.findContours(
            threshold, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


        # list for storing names of shapes
        for contour in contours:

            # cv2.approxPloyDP() function to approximate the shape
            approx = cv.approxPolyDP(
                contour, 0.0175 * cv.arcLength(contour, True), True)

            # putting shape name at center of each shape
            if len(approx) == 4:
                cv.drawContours(frame, [contour], 0, (0, 255, 255), -1)
                area = cv.contourArea(contour)
                if area > 1000:
                    cv.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv.putText(frame, 'D', (contour[0][0][0], contour[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)
                
                M = cv.moments(contour)
                if M['m00'] != 0:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cv.drawContours(frame, [i], -1, (0, 255, 0), 2)
                    cv.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
                    cv.putText(frame, "center", (cx - 20, cy - 20),
	        			cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                print(f"x: {cx} y: {cy}")

            else:
                area = cv.contourArea(contour)
                if area > 1000:
                    cv.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv.putText(frame, 'Y', (contour[0][0][0], contour[0][0][1]), cv.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

                    M = cv.moments(contour)
                    if M['m00'] != 0:
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        cv.drawContours(frame, [i], -1, (0, 255, 0), 2)
                        cv.circle(frame, (cx, cy), 7, (0, 0, 255), -1)
                        cv.putText(frame, "center", (cx - 20, cy - 20),
	                			cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                print(f"x: {cx} y: {cy}")
       

        # displaying the image after drawing contours
        cv.imshow('shapes', frame)

        cv.waitKey(1)
        #cv2.destroyAllWindows()