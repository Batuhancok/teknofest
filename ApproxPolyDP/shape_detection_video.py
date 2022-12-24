import cv2
import numpy as np

# reading image
cap = cv2.VideoCapture('Shapes Song.mp4')


while (cap.isOpened()):

    ret, frame = cap.read()
    if ret == True:
            
        # converting image into grayscale image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # setting threshold of gray image
        _, threshold = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)
        #erode_threshold = cv2.erode(threshold, (5,5), iterations=2)

        cv2.imshow('thresh', threshold)
        cv2.waitKey(1)

        # using a findContours() function
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


        # list for storing names of shapes
        for contour in contours:

            # cv2.approxPloyDP() function to approximate the shape
            approx = cv2.approxPolyDP(
                contour, 0.0175 * cv2.arcLength(contour, True), True)

            # putting shape name at center of each shape
            if len(approx) <= 8:
                cv2.drawContours(frame, [contour], 0, (0, 255, 255), -1)

            else:
                area = cv2.contourArea(contour)
                if area > 1000:
                    cv2.drawContours(frame, [contour], 0, (255, 0, 0), -1)
                    cv2.putText(frame, 'X', (contour[0][0][0], contour[0][0][1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 2)

        # displaying the image after drawing contours
        cv2.imshow('shapes', frame)

        cv2.waitKey(1)
        #cv2.destroyAllWindows()